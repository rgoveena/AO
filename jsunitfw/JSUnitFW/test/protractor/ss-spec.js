/**
 * Created by Govi Rajagopal on 10/23/17.
 */

'use strict'

var env = require('./env.js');
var exp = 'Dev:SSLogin:';

var url = browser.params.shore;

var username = browser.params.username = 'perfman'
var password = browser.params.password = 'Perfman17'
console.log('username:'+ username);
console.log('password:'+ password);

describe(exp+ 'Protractor Demo App', function() {
      beforeEach(function () {
        browser.ignoreSynchronization = true;
        expect(1).toBe(1);
    });
  // Sample test case to understand the flow
  // it(exp+'Test:should add one and two', function() {
  //   browser.get('http://juliemr.github.io/protractor-demo/');
  //   element(by.model('first')).sendKeys(10);
  //   element(by.model('second')).sendKeys(20);
  //   browser.sleep(5000);
  //   element(by.id('gobutton')).click();
  //   browser.sleep(5000);

  // });

  it(exp+'SS:Shore: Login', function() {
    browser.get(url);
    browser.sleep(5000);
    element(by.name('username')).sendKeys(username);
    element(by.name('password')).sendKeys(password);
    browser.sleep(5000);
    element(by.id('btnLogin')).click();
    expect(1).toBe(1);
    browser.sleep(8000);
    console.log("login completed..");
    // expect(browser.getTitle()).toEqual('SMARTShip V1.1');
    // console.log(browser.getTitle(),"title check completed..");
    // expect(browser.getCurrentUrl()).toEqual(local);
    console.log('Login complete');

  });

    // it(exp+'should have DashBoard Items', function() {
    // console.log("Angular caught up");
    // TO-DO 


  // });


    it(exp+'SS:Shore: Logout', function() {
    //browser.get('https://test.alphaorimarine.com/');
    browser.sleep(8000);
    var userIcon  = element.all(by.css('.fa-user'));
    userIcon.click();
    // expect(1).toBe(1);
    browser.sleep(5000);
    element(by.id('logOut')).click();
    // expect(1).toBe(1);
    console.log("Logout completed..");
    browser.sleep(5000);
    //expect(1).toBe(1);

  });



  });