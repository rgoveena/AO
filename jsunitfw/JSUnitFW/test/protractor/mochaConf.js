/**
 * Created by Govi Rajagopal on 10/27/17.
 */
var env = require('./env.js');

// A small suite to make sure the mocha framework works.
exports.config = {
  seleniumAddress: env.seleniumAddress,

  framework: 'mocha',

  // Spec patterns are relative to this directory.
  specs: [
    'mocha/*_spec.js'
  ],

  capabilities: env.capabilities,

  baseUrl: env.baseUrl + '/home',

  mochaOpts: {
    reporter: 'spec',
    timeout: 4000
  }
};
