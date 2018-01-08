<?php
/* ====================================================================
 * Copyright (C) BluePex Security Solutions - All rights reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by  Bruno B. Stein <bruno.stein@bluepex.com>, 2015
 * Written by  Francisco Cavalcante <francisco.cavalcante@bluepex.com>, 2015
 *
 * ====================================================================
 *
 */
 
require("config.inc");

define(DEBUG, false);
define(WSUTM_CACHE_FILE, "{$g['tmp_path']}/wsutm.cache");

function do_webservice_request($service, $method, $params = array()) {
	// Set limit to 0 for CURLOPT_CONNECTTIMEOUT
	set_time_limit(0);

	$url = "http://wsutm.bluepex.com/api/{$service}/{$method}";

	$data = array(
		"serial" => file_exists('/etc/serial') ? trim(file_get_contents('/etc/serial')) : '',
		"product_key" => getProductKey(),
	);

	if (!empty($params)) {
		$data = array_merge($data, $params);
	}

	$ch = curl_init($url);
	if (is_resource($ch)) {
		curl_setopt($ch, CURLOPT_POST, true);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 4);
		if (DEBUG)
			curl_setopt($ch, CURLOPT_VERBOSE, true);

		$result = curl_exec($ch);
		curl_close($ch);
		
		if (empty($result))
			return "error";

		$ret = json_decode($result);
		if(empty($ret))
			return "error";
		return $ret->response;
	}
}

function getProductKey() {
	$command = "/usr/local/sbin/dmidecode -t 4 | grep ID | sed 's/.*ID://;s/ //g'";
	$gc = exec($command, $out, $err);
	if ($err == 0) {
		return $out[0];
	} else {
		return '';
	}
}

function send_serial_productkey() {
	$resp = do_webservice_request('util', 'insert-serial-productkey');

	if ( ($resp->status != 'ok') )
		log_error(dgettext("BPBackup", "Error to server validate serial and productkey."));
}

function create_wsutm_cache_file() {
	$data = array();
	$data['expire'] = time() + 24 * 60 * 60;

	$resp = do_webservice_request("serial", "info");
	if (isset($resp->data) && !empty($resp->data)) {
		$data['serial'] = $resp->data;
	}
	if (file_put_contents(WSUTM_CACHE_FILE, serialize($data))) {
		return true;
	}
	return false;
}

function read_wsutm_cache_file() {
	if (!file_exists(WSUTM_CACHE_FILE)) {
		create_wsutm_cache_file();
	}
	if (file_exists(WSUTM_CACHE_FILE)) {
		$content = unserialize(file_get_contents(WSUTM_CACHE_FILE));
		if (isset($content['expire']) && $content['expire'] <= time()) {
			unlink(WSUTM_CACHE_FILE);
			$content = read_wsutm_cache_file();
		}
		return $content;
	}
}

function get_serial_status() {
	$data = read_wsutm_cache_file();
	$serial_status = "ok";
	if (!isset($data['serial']) || (isset($data['serial']->overdue) && $data['serial']->overdue == "1")) {
		$serial_status = "irregular";
	} elseif (isset($data['serial']->cancelled) && $data['serial']->cancelled == "1") {
		$serial_status = "cancelled";
	}
	return $serial_status;
}

function check_serial_status() {
	$status = get_serial_status();
	if ($status !== "ok") {
		set_flash_message("warning", "<i class='fa fa-warning'></i> " . sprintf(gettext("The Serial Number assigned to this UTM is '%s'! To avoid the stopping of the services, please contact the BluePex Support Team for further information."), strtoupper($status)));
	}
}

function redirect_licensed_area($area_id = "") {
	$status = get_serial_status();
	if ($status === "ok") {
		return;
	}
	if (!empty($area_id)) {
		$exec_function_cancelled_serial = "{$area_id}_cancelled_serial";
		$exec_function_irregular_serial = "{$area_id}_irregular_serial";

		if ($status === "cancelled" && function_exists($exec_function_cancelled_serial)) {
			$exec_function_cancelled_serial();
		}
		if ($status === "irregular" && function_exists($exec_function_irregular_serial)) {
			$exec_function_irregular_serial();
		}
	}
	header("Location: /bluepex_license_control.php?serial_status={$status}");
	exit;
}
