/**
 * Module for T_DESCRIPTION_HERE.
 */
let restconf = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        progressbar: null,
        swagmodel: 'div#ys-load-model',
    };

    let c = config;     // internal alias for brevity

    function getSwagStatus(names, yangset) {
        if (!names || !yangset) {
            return;
        }

        yangsuite.startProgress($(c.progressbar), '/restconf/getstatus/');
    }
    /**
     * Public API.
     */
    return {
        config:config,
        getSwagStatus:getSwagStatus,
    };
}();
