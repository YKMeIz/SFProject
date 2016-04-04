#!/usr/bin/env php
<?php
/**
 * Fedora Drupal 8 RPM find provides.
 *
 * Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * @copyright Copyright (c) 2016, Shawn Iwinski <shawn@iwin.ski>
 * @license http://opensource.org/licenses/MIT MIT
 */
namespace FedoraDrupal8Rpmbuild;

require_once '__PHPDIR__/Symfony/Component/Console/autoload.php';
require_once '__PHPDIR__/Symfony/Component/Yaml/autoload.php';

use Symfony\Component\Console\Application;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Yaml\Yaml;

/**
 * Outputs Drupal 8 virtual provides from files provided via STDIN.
 */
class FindProvides extends Command
{
    /**
     * Configures command.
     */
    protected function configure()
    {
        $this
            ->setName('find-provides')
            ->setDescription('Finds RPM drupal8(*) and php-composer(*) virtual provides')
            // --spec-version
            ->addOption(
                'spec-version',
                null,
                InputOption::VALUE_REQUIRED,
                'RPM spec version'
            );
    }

    /**
     * Outputs Drupal 8 virtual provides from files provided via STDIN.
     *
     * Sorts unique values from {@link executeDrupal8()} and
     * {@link executeComposer()}.  If "--spec-version" option is provided,
     * outputs each virtual provide with its' value.
     *
     * @param InputInterface  $input  An InputInterface instance.
     * @param OutputInterface $output An OutputInterface instance.
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $file = trim(fgets(STDIN));
        if (empty($file) || !is_file($file)) {
            return;
        }

        $provides = [];

        if (
            empty($fileProvides = $this->executeDrupal8($file))
            && empty($fileProvides = $this->executeComposer($file))
        ) {
            return;
        }

        if (is_array($fileProvides)) {
            $provides = array_merge($provides, $fileProvides);
        } else {
            $provides[] = $fileProvides;
        }

        $specVersion = $input->getOption('spec-version');
        $useSpecVersion = !empty($specVersion) || ('0' === $specVersion);

        foreach ($provides as $p) {
            $output->write($p);
            $output->writeln($useSpecVersion ? ' = '.$specVersion : '');
        }
    }

    /**
     * Returns drupal8(*) virtual provide from a *.info.yml file.
     *
     * @param string $file A file name (full path).
     *
     * @return string|null drupal8(*) virtual provide or null
     */
    private function executeDrupal8($file)
    {
        if (!preg_match('/\.info\.yml$/', $file)) {
            return;
        }

        // Hidden?
        $info = Yaml::parse(file_get_contents($file));
        if (!empty($info['hidden'])) {
            return;
        }

        return sprintf('drupal8(%s)', basename($file, '.info.yml'));
    }

    /**
     * Returns php-composer(*) virtual provides from a composer.json file.
     *
     * Returns values from the following Composer properties:
     * - {@link https://getcomposer.org/doc/04-schema.md#name name}
     * - {@link https://getcomposer.org/doc/04-schema.md#replace replace}
     *     - Values are only returned if their version equals "self.version"
     *
     * @param string $file A file name (full path).
     *
     * @return array|null php-composer(*) virtual provides or null
     */
    private function executeComposer($file)
    {
        if ('composer.json' != basename($file)) {
            return;
        }

        $info = json_decode(file_get_contents($file), true);
        $provides = [$info['name']];

        if (!empty($info['replace'])) {
            foreach ($info['replace'] as $name => $version) {
                if ('self.version' == $version) {
                    $provides[] = $name;
                }
            }
        }

        return array_map(function ($p) {
            return sprintf('php-composer(%s)', $p);
        }, $provides);
    }
}

// Create application, add command, and run
$application = new Application('Fedora Drupal 8 RPM find provides', '__SPEC_VERSION__-__SPEC_RELEASE__');
$application->add(new FindProvides());
$application->run();
