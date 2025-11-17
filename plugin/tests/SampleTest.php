<?php
/**
 * Sample test case
 *
 * @package {{PACKAGE_NAME}}
 */

namespace {{NAMESPACE}}\Tests;

use WP_Mock\Tools\TestCase;

/**
 * Sample test class
 */
class SampleTest extends TestCase {

	/**
	 * Set up test
	 */
	public function setUp(): void {
		\WP_Mock::setUp();
	}

	/**
	 * Tear down test
	 */
	public function tearDown(): void {
		\WP_Mock::tearDown();
	}

	/**
	 * Sample test method
	 */
	public function test_sample() {
		$this->assertTrue( true );
	}
}
