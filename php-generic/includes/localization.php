<?php

/*
 * Define APPLICATION_ROOT constant here.
 * 
 * The constant is used in include's and require's 
 * across the code of the library.
 *
 */
define('APPLICATION_ROOT', $_SERVER['DOCUMENT_ROOT']);


/*
 * Make $supported_locales available.
 *
 * Edit this array to add/remove locales.
 * 
 */
require_once APPLICATION_ROOT . "/config/supported_locales.config.php";

require_once APPLICATION_ROOT . "/lib/Localization.class.php";
$localization = new Localization($supported_locales);
$locale = $localization->init();

?>
