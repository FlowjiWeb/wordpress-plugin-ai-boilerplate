<?php
/**
 * PHPUnit bootstrap file
 *
 * @package {{PACKAGE_NAME}}
 */

// Load WP_Mock
require_once dirname( __DIR__ ) . '/vendor/autoload.php';

// Bootstrap WP_Mock
WP_Mock::bootstrap();
