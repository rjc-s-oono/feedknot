/**
 * jQuery Logging Plugin.
 *
 * Version 0.8
 *
 * Created by saotii
 * 29 March 2014
 *
 * Usage:
 *
 *   var logger = $(window).logging({requestUrl: "http://localhost/log"});
 *   logger.error("error message!!");
 *   logger.debug("debug message.");
 *
 * History:
 *
 *   0.80 - Released (29 March 2014)
 *
 * License:
 *
 *   This plugin is licensed under the GNU General Public License: http://www.gnu.org/licenses/gpl.html
 *
 */
;(function($) {

    var plugname = 'logging';

    /**
     * インナークラス共通コンストラクタ
     */
    var LoggerClass = function(elem, params){
        this.elem = elem;
        this.params = params;
    }

    function logTransfer(loglevel, message, opts) {
        transferData = {
            'loglevel' : loglevel,
            'message' : message
        }

        $.ajax({
            global : 'false',
            type : 'POST',
            url : opts.requestUrl,
            data : transferData,
            dataType : 'json'
        });

        if (opts.debug && typeof window.console !== "undefined") {
            console.log('['+loglevel+']:'+message);
        }
    };

    LoggerClass.prototype.fatal = function(message){
        logTransfer('FATAL', message, this.params);
        return this;
    };
    LoggerClass.prototype.error = function(message) {
        logTransfer('ERROR', message, this.params);
        return this;
    };
    LoggerClass.prototype.warn = function(message) {
        logTransfer('WARN', message, this.params);
        return this;
    };
    LoggerClass.prototype.info = function(message) {
        logTransfer('INFO', message, this.params);
        return this;
    };
    LoggerClass.prototype.debug = function(message) {
        logTransfer('DEBUG', message, this.params);
        return this;
    };
    LoggerClass.prototype.trace = function(message) {
        logTransfer('TRACE', message, this.params);
        return this;
    };

    var defaults = {
        debug: false,
        requestUrl: null
    };

    $.fn[plugname] = function(options){
        return new LoggerClass(this, $.extend(defaults, options));
    }
})(jQuery);