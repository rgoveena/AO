var express = require('express');
var router = express.Router();
const path = require('path');
const cors = require('./cors');
const fs = require('fs');
//const pyshell = require('python-shell')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

//NODE TO PYTHON TO CASSANDRA PRE-BUILT QUERY

router.route('/python/:file/:host')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	//console.log("Node calling "+req.params.file+" python script with "+req.params.host);
	if (fs.existsSync('python-scripts/'+req.params.file)){
		console.log(req.params.file+ 'found in python-scripts folder');
	} else {
		console.log(req.params.file+ 'not found');
	}
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/'+req.params.file, req.params.host]);
	pythonProcess.stdout.on('data', (data) => {
	    res.send(data.toString().split("\n")); //converting python text to a list of strings to easily render in ReactList
	});
});

router.route('/connect/:host')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	//console.log("Node calling cassandra-connect python script with "+req.params.host);
	if (fs.existsSync('python-scripts/cassandra-connect.py')){
		console.log('cassandra-connect.py found in python-scripts folder');
	} else {
		console.log('cassandra-connect.py not found');
	}
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/cassandra-connect.py', req.params.host]);
	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString());
	    res.send(data.toString()); 
	});
});

//NODE TO PYTHON TO CASSANDRA CUSTOM QUERY

router.route('/custom/:query/:host')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	//console.log("Node calling custom-query python script with host "+req.params.host+" and query "+req.params.query);
	if (fs.existsSync('python-scripts/custom-query.py')){
		console.log('custom-query.py found in python-scripts folder');
	} else {
		console.log('custom-query.py not found');
	}
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/custom-query.py', req.params.query, req.params.host]);
	pythonProcess.stdout.on('data', (data) => {
	    res.send(data.toString().split("\n")); //converting python text to a list of strings to easily render in ReactList
	});
});

router.route('/ms/:reqType/:url/:resLength')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	if (fs.existsSync('python-scripts/ms.py')){
		console.log('ms.py found in python-scripts folder');
	} else {
		console.log('ms.py not found');
	}
	var url = decodeURI(req.params.url);
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/ms.py', req.params.reqType, url, req.params.resLength]);
	pythonProcess.stdout.on('data', (data) => {
		//console.log(data.toString())
	    res.send(data.toString().split("\n")); //converting python text to a list of strings to easily render in ReactList
	});
});

router.route('/api/:method/:hostUrl/:signature')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	if (fs.existsSync('python-scripts/api.py')){
		console.log('api.py found in python-scripts folder')
	} else {
		console.log('api.py not found')
	}
	var signature = decodeURI(req.params.signature);
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/api.py', req.params.method, req.params.hostUrl, signature]);
	pythonProcess.stdout.on('data', (data) => {
		//console.log(data.toString())
	    res.send(data.toString().split("\n")); //converting python text to a list of strings to easily render in ReactList
	});
})
.post(cors.cors, (req,res,next) => {
	if (fs.existsSync('python-scripts/api.py')){
		console.log('api.py found in python-scripts folder')
	} else {
		console.log('api.py not found')
	}
	var content = req.body.content;
	var signature = decodeURI(req.params.signature);
	const spawn = require("child_process").spawn;
	const pythonProcess = spawn('python',['python-scripts/api.py', req.params.method, req.params.hostUrl, signature, content]);
	pythonProcess.stdout.on('data', (data) => {
		console.log(data.toString());
	    res.send(data.toString().split("\n")); //converting python text to a list of strings to easily render in ReactList
	});
});


router.route('/upload')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.post(cors.cors, (req, res, next) => {
	if (fs.existsSync('python-scripts/plot.py')){
		console.log('plot.py found in python-scripts folder')
	} else {
		console.log('plot.py not found')
	}
 	
 	/*
	if (fs.existsSync('python-scripts/uploaded-files/'+req.body.filename+'.csv')) {
		fs.unlink('python-scripts/uploaded-files/'+req.body.filename+'.csv', (err) => {
			if (err) {
				console.error(err)
			}
			else {
				console.log("csv file deleted")
			}
		})
	}

	if (fs.existsSync('public/graphs/'+req.body.filename+'.png')) {
		fs.unlink('public/graphs/'+req.body.filename+'.png', (err) => {
			if (err) {
				console.error(err)
			}
			else {
				console.log("png file deleted")
			}
		})
	}
	*/

 	var file = req.files.file;
	file.mv(`python-scripts/uploaded-files/${req.body.filename}.csv`, function(err) {
	    if (err) {
	      return res.status(500).send(err);
	    }
	    const spawn = require("child_process").spawn;
		const pythonProcess = spawn('python',['python-scripts/plot.py', req.body.filename]);
		pythonProcess.stdout.on('data', (data) => {
		    res.send(data.toString()); 
		});
	  })
});


//CASSANDRA FROM NODE
/*
var PlainTextAuthProvider = cassandra.auth.PlainTextAuthProvider;
var client = new cassandra.Client({ contactPoints:['127.0.0.1:9042'], 
                                    authProvider: new PlainTextAuthProvider('cassandra', 'cassandra'),
                                	keyspace: 'smartship_shore'});

const hardcode_query = 'SELECT * FROM company';

router.route('/cassandra/:query')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req,res,next) => {
	client.execute(hardcode_query, function(err, result) {
		console.log('database result: ', result);
	    if (err) {
	      console.log('\n' + err);
	    }
	})
});
*/


module.exports = router;
