#!/usr/bin/env php
<?php
/**
 * Fedora Drupal 8 RPM modify core's composer.json.
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

use Symfony\Component\Console\Application;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;

/**
 *
 */
class ModifyCoreComposerJson extends Command
{
    protected function configure()
    {
        $this
            ->setName('modify-core-composer-json')
            ->setDescription('Modifies core/composer.json')
            ->addOption(
                'builddir',
                null,
                InputOption::VALUE_REQUIRED,
                'RPM build dir (RPM macro "%{_builddir}")',
                __DIR__
            );
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $composerJsonFile = $input->getOption('builddir').'/core/composer.json';
        $this->executeDistCopy($input, $output, $composerJsonFile);
        $composerJsonDecoded = $this->executeDecode($input, $output, $composerJsonFile);

        // Empty "require", "require-dev", and "scripts"
        //unset($composerJsonDecoded['require']);
        //unset($composerJsonDecoded['require-dev']);
        //unset($composerJsonDecoded['scripts']);

        // Modify "autoload" "files" to include de-coupled libraries' autoloaders
        $composerJsonDecoded['autoload']['files'] = array_merge(
            $composerJsonDecoded['autoload']['files'],
            array(
                '__PHPDIR__/Composer/Semver/autoload.php',
                '__PHPDIR__/Doctrine/Common/Annotations/autoload.php',
                '__PHPDIR__/Doctrine/Common/autoload.php',
                '__PHPDIR__/EasyRdf/autoload.php',
                '__PHPDIR__/Egulias/EmailValidator/autoload.php',
                '__PHPDIR__/GuzzleHttp6/autoload.php',
                '__PHPDIR__/Masterminds/HTML5/autoload.php',
                '__PHPDIR__/Stack/autoload-builder.php',
                '__PHPDIR__/Symfony/Bridge/PsrHttpMessage/autoload.php',
                '__PHPDIR__/Symfony/Cmf/Component/Routing/autoload.php',
                '__PHPDIR__/Symfony/Component/ClassLoader/autoload.php',
                '__PHPDIR__/Symfony/Component/Console/autoload.php',
                '__PHPDIR__/Symfony/Component/DependencyInjection/autoload.php',
                '__PHPDIR__/Symfony/Component/EventDispatcher/autoload.php',
                '__PHPDIR__/Symfony/Component/HttpFoundation/autoload.php',
                '__PHPDIR__/Symfony/Component/HttpKernel/autoload.php',
                '__PHPDIR__/Symfony/Component/Process/autoload.php',
                '__PHPDIR__/Symfony/Component/Routing/autoload.php',
                '__PHPDIR__/Symfony/Component/Serializer/autoload.php',
                '__PHPDIR__/Symfony/Component/Translation/autoload.php',
                '__PHPDIR__/Symfony/Component/Validator/autoload.php',
                '__PHPDIR__/Symfony/Component/Yaml/autoload.php',
                '__PHPDIR__/Twig/autoload.php',
                '__PHPDIR__/Zend/autoload.php',
                '__PHPDIR__/Zend/Diactoros/autoload.php',
            )
        );

        $this->executeEncode($input, $output, $composerJsonFile, $composerJsonDecoded);
    }

    protected function executeDistCopy(InputInterface $input, OutputInterface $output, $composerJsonFile)
    {
        // Copy composer.json to composer.json.dist
        $composerJsonFileDist = $composerJsonFile.'.dist';
        $output->writeln(sprintf(
          'Copying "%s" to "%s"...',
          $composerJsonFile,
          $composerJsonFileDist
        ));
        if (!copy(
            $composerJsonFile,
            $composerJsonFileDist
        )) {
            throw new \Exception(sprintf(
              'Failed to copy "%s" to "%s"',
              $composerJsonFile,
              $composerJsonFileDist
            ));
        }
    }

    protected function executeDecode(InputInterface $input, OutputInterface $output, $composerJsonFile)
    {
        // Read composer.json
        $output->writeln(sprintf('Reading "%s"...', $composerJsonFile));
        $composerJsonContents = file_get_contents($composerJsonFile);
        if (false === $composerJsonContents) {
            throw new \Exception(sprintf('Failed to read "%s"', $composerJsonFile));
        }

        // Decode composer.json
        $output->writeln(sprintf('Decoding "%s"...', $composerJsonFile));
        $composerJsonDecoded = json_decode($composerJsonContents, true);
        if (null === $composerJsonDecoded) {
            throw new \Exception(sprintf('Failed to parse "%s"', $composerJsonFile));
        }

        return $composerJsonDecoded;
    }

    protected function executeEncode(InputInterface $input, OutputInterface $output, $composerJsonFile, array $composerJsonDecoded)
    {
        // Encode composer.json contents
        $output->writeln(sprintf('Encoding "%s"...', $composerJsonFile));
        $composerJsonEncoded = json_encode($composerJsonDecoded, JSON_PRETTY_PRINT);
        if (false === $composerJsonEncoded) {
            throw new \Exception(sprintf('Failed to encode "%s"', $composerJsonFile));
        }

        // Re-write composer.json
        $output->writeln(sprintf('Writing "%s"...', $composerJsonFile));
        if (false === file_put_contents($composerJsonFile, $composerJsonEncoded)) {
            throw new \Exception(sprintf('Failed to write "%s"', $composerJsonFile));
        }
    }
}

// Create application, add command, and run
$application = new Application('Fedora Drupal 8 RPM modify core\'s composer.json', '__SPEC_VERSION__-__SPEC_RELEASE__');
$application->add(new ModifyCoreComposerJson());
$application->run();
