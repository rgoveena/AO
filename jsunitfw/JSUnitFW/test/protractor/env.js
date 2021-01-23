'use strict'

/**
 * Created by Govi Rajagopal on 10/24/2017.
 *

// This can be changed via the command line as:
// --params.username 'admin'
// --params.base_url 'https://18.220.212.10'


browser.params.username = 'admin'
browser.params.password = '1'

// Add your gateways and ports
browser.params.local = 'http://localhost:8080'

// Add your urls in here...
browser.params.shore_url = 'https://test.alphaorimarine.com/'
browser.params.ship_url = 'http://182.156.249.218:3030/home'

*/

browser.params.username = 'perfman'
browser.params.password = 'Perfman17'

browser.params.shore = 'https://test.alphaorimarine.com'
browser.params.ship = 'http://182.156.249.218:3030'
//var local = 'https://test.alphaorimarine.com'


var webServerDefaultPort = 8081;


var userIcon  = element.all(by.css('.fa-user'));
var settingsIcon = element.all(by.css('.settings-icon'));
//var settingsIcon = element.all(by.xpath('/html/body/app-root/app-home/nav/div[2]/ul/li[1]/a/span[1]'));




module.exports = {
  // The address of a running selenium server.
  seleniumAddress:
    (process.env.SELENIUM_URL || 'http://localhost:4444/wd/hub'),

  // Capabilities to be passed to the webdriver instance.
  capabilities: {
    'browserName':
        (process.env.TEST_BROWSER_NAME || 'chrome'),
    'version':
        (process.env.TEST_BROWSER_VERSION || 'ANY')
  },

  // Default http port to host the web server
  webServerDefaultPort: webServerDefaultPort,

  // Protractor interactive tests
  interactiveTestPort: 6969,

  // A base URL for your application under test.
  baseUrl:
    'http://' + (process.env.HTTP_HOST || 'localhost') +
          ':' + (process.env.HTTP_PORT || webServerDefaultPort)

};

