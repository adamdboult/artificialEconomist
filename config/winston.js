var winston = require('winston');
//winston.emitErrs = true;

var logger = winston.createLogger({

    transports: [
        new winston.transports.File({
            level: 'debug',
            filename: __dirname+'/../winston.log',
            handleExceptions: true,
            json: true,
            colorize: false
        }),
        new winston.transports.Console({
            level: 'debug',
            handleExceptions: true,
            json: false,
            colorize: true
        })
    ],
    exitOnError: false
});
module.exports=logger;
