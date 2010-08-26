<?php

/* i18n
 *
 * Licence: MPL 2/GPL 2.0/LGPL 2.1
 * Author: Stas Malolepszy, Mozilla
 * Date : 2010-07-17
 *
 * Description:
 *
 * This class will handle locale detection and enable
 * gettext support for your webapp.
 *
 */




class Localization
{

    public $supported_locales;
    public $locale_chooser;

    public function __construct($list=array('en-US')) {
        $this->supported_locales = array_unique($list);
        require_once APPLICATION_ROOT . "/lib/ChooseLocale.class.php";
        $this->locale_chooser = new ChooseLocale(array_keys($this->supported_locales));
    }

    public function init() {
        if (array_key_exists("locale", $_GET) &&
            array_key_exists($_GET["locale"], $this->supported_locales)) {
            $locale = $_GET["locale"];
            setlocale(LC_ALL, $this->supported_locales[$locale]);
            bindtextdomain("messages", APPLICATION_ROOT . "/locale");
            bind_textdomain_codeset("messages", "UTF-8");
            textdomain("messages");
            return $locale;
        } else {
            $locale = $this->locale_chooser->getCompatibleLocale();
            $url = $this->create_localized_url($locale);
            $this->no_caching_redirect($url);
        }
    }

    public function create_localized_url($locale_code) {
        $url = parse_url($_SERVER['SCRIPT_URI']);
        // By using $requested_page instead of $url['path'] we avoid
        // potential infinite loops in case the user goes to a URL
        // with an unsupported locale in it, e.g. /xx/foo/. In this
        // example $requested_page would be "/foo/" which is what we want.
        $requested_page = rtrim($_SERVER['SCRIPT_NAME'], 'index.php');
        return $url['scheme'] .'://'. $url['host'] .'/'. $locale_code . $requested_page;
    }

    public function no_caching_redirect($url) {
        header('Date: '.gmdate('D, d M Y H:i:s \G\M\T', time()));
        header('Expires: Fri, 01 Jan 1990 00:00:00 GMT');
        header('Pragma: no-cache');
        header('Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0, private');
        header('Vary: *');
        header('Location: '. $url);
        exit();
    }

}

?>
