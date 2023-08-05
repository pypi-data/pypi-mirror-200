from distutils.core import setup
setup(
	name = 'pi_MCP342x',         # How you named your package folder (MyLib)
	packages = ['pi_MCP342x'],   # Chose the same as "name"
	version = '0.1',      # Start with a small number and increase it with every change you make
	license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
	description = 'Python module to use the MCP342x series of ADCs with the Raspberry Pi',   # Give a short description about your library
	author = 'Sergio Caponi',                   # Type in your name
	author_email = 'contactme@sergiocaponi.com',      # Type in your E-Mail
	url = 'https://github.com/sergiocaponi/pi_MCP342x',   # Provide either the link to your github or to your website
	download_url = 'https://github.com/sergiocaponi/pi_MCP342x/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
	keywords = ['Raspberry Pi', 'ADC', 'MCP342x', 'MCP3422', 'MCP3423', 'MCP3424'],   # Keywords that define your package best
	install_requires=[            # I get to this in a second
					'smbus2',
			],
	classifiers=[
		'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers',      # Define that your audience are developers
		'Operating System :: POSIX :: Linux',
		'Topic :: Software Development :: Build Tools',
		'Topic :: System :: Hardware',
		'License :: OSI Approved :: MIT License',   # Again, pick a license
		'Programming Language :: Python :: 3',
	],
)