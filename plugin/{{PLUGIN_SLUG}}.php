<?php
/**
 * Plugin Name: {{PLUGIN_NAME}}
 * Plugin URI: {{PLUGIN_URI}}
 * Description: {{PLUGIN_DESCRIPTION}}
 * Version: 1.0.0
 * Author: {{AUTHOR_NAME}}
 * Author URI: {{AUTHOR_URI}}
 * License: GPL-2.0+
 * License URI: http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain: {{TEXT_DOMAIN}}
 * Domain Path: /languages
 *
 * @package {{PACKAGE_NAME}}
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}

/**
 * Currently plugin version.
 * Start at version 1.0.0 and use SemVer - https://semver.org
 */
define( '{{CONSTANT_PREFIX}}_VERSION', '1.0.0' );
define( '{{CONSTANT_PREFIX}}_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( '{{CONSTANT_PREFIX}}_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

/**
 * The code that runs during plugin activation.
 */
function activate_{{FUNCTION_PREFIX}}() {
	require_once {{CONSTANT_PREFIX}}_PLUGIN_DIR . 'includes/class-{{PLUGIN_SLUG}}-activator.php';
	{{NAMESPACE}}\Activator::activate();
}

/**
 * The code that runs during plugin deactivation.
 */
function deactivate_{{FUNCTION_PREFIX}}() {
	require_once {{CONSTANT_PREFIX}}_PLUGIN_DIR . 'includes/class-{{PLUGIN_SLUG}}-deactivator.php';
	{{NAMESPACE}}\Deactivator::deactivate();
}

register_activation_hook( __FILE__, 'activate_{{FUNCTION_PREFIX}}' );
register_deactivation_hook( __FILE__, 'deactivate_{{FUNCTION_PREFIX}}' );

/**
 * The core plugin class.
 */
require {{CONSTANT_PREFIX}}_PLUGIN_DIR . 'includes/class-{{PLUGIN_SLUG}}.php';

/**
 * Begins execution of the plugin.
 */
function run_{{FUNCTION_PREFIX}}() {
	$plugin = new {{NAMESPACE}}\Plugin();
	$plugin->run();
}
run_{{FUNCTION_PREFIX}}();
