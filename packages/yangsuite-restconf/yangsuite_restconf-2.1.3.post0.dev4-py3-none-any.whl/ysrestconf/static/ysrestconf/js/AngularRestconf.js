'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('AngularRestconf', ['ngSanitize', 'ngRoute', 'swaggerUi', 'ui.bootstrap']);

app.controller('MainCtrl', function ($scope, $http, $sce, $location) {

	$scope.show_swagger_ui = false;
	$scope.show_api_button = false;
	$scope.show_more_button = false;
	$scope.show_clear_button = false;

	$scope.ClearSwagger = function() {
		$scope.show_swagger_status = false;
		$scope.show_swagger_ui = false;
		$scope.show_api_button = false;
		$scope.show_more_button = false;
		$scope.swagOverFlow = {};
	}

	function getHead(swagobj) {
		let swagHead = {}

		for (let key of Object.keys(swagobj)) {
			if (key != "paths") {
				swagHead[key] = swagobj[key];
			}
		}
		swagHead["paths"] = getNextGroup(swagobj["paths"], 50);
		return swagHead;
	}

	function getNextGroup(swagobj, count) {
		let paths = {};
		let keys = Object.keys(swagobj);

		if (keys && keys.length < count) {
			count = keys.length;
		}

		if (!keys || !keys.length > 0) {
			$scope.show_more_button = false;
			return;
		}

		for (let i = 0; i < count; i++) {
			paths[keys[i]] = swagobj[keys[i]];
			delete swagobj[keys[i]];
		}

		return paths;
	}

	$scope.ShowMoreAPIs = function() {
		if ($scope.swagOverFlow) {
			if ($scope.swagOverFlow.paths) {
				$scope.swagObj = getHead($scope.swagOverFlow);
			}
		}
		let pathNum = Object.keys($scope.swagOverFlow.paths).length;
		let text = "Load " + pathNum + " more APIs";
		$("#ys-more-apis").text(text);
		if (pathNum == 0) {
			$scope.numPath = 0;
			$scope.show_more_button = false;
			$("#ys-warn-dialog")
	        .empty()
	        .dialog({
	            title: "All APIs Shown",
	            minHeight: 100,
	            maxWidth: 200,
	            buttons: {
	            	"Close": function () {
	            		$(this).dialog("close");
	            	},
	            }
	        })
	        .html('<pre>')
	        .append('All RESTCONF APIs have been shown.\n',
	        	    'If you wish to cycle through again,\n',
	        	    'click on "Generate APIs". You can also\n',
	        	    'search the module for a different branch\n',
	        	    'of APIs to generate.</pre>')
	        .dialog("open");
		}
	}

	function LoadAPIs(swagobj) {
        $scope.swagOverFlow = swagobj;
		$scope.show_swagger_ui = true;
		$scope.swagObj = getHead($scope.swagOverFlow);
		let pathNum = Object.keys($scope.swagOverFlow.paths).length;
		if (pathNum) {
			let text = "Load " + pathNum + " more APIs"
		    $("#ys-more-apis").text(text);
		    $scope.show_more_button = true;
		}
		stopProgress($("#ys-progress"));
	}

	$scope.LoadSchema = function() {
		$scope.show_more_button = false;
		let csrf = Cookies.get('csrftoken');
		let yangset = $("#ytool-yangset").val();
		let device = $("#ytool-devices").val();
		let nodeIds = $("#tree").jstree(true).get_selected();
		let nodeData = [];
		let scopeModels = $scope.models;
		if (nodeIds.length > 0) {
			scopeModels = [];
		}
		$.each(nodeIds, function(i, n) {
			if (n != 1) {
			    let node = $("#tree").jstree(true).get_node(n);
				nodeData.push(node.data);
				let nodeParent = node.parents[node.parents.length - 2];
				let nodeModel = $("#tree").jstree(true).get_node(nodeParent);
				scopeModels.push(nodeModel.text);
			}
		});
		let params = {
			"models": scopeModels,
			"yangset": yangset,
			"device": device,
			"nodes": nodeData,
			"host": location.hostname + ':' + location.port
		};

		if (nodeData.length == 0) {
	        $("#ys-warn-dialog")
	        .empty()
	        .dialog({
	            title: "WARNING",
	            minHeight: 100,
	            maxWidth: 200,
	            buttons: {
	                "Continue": function () {
	                    $(this).dialog("close");
	                    let config = {
                            method: "GET",
					        url: $sce.trustAsResourceUrl('/restconf/genswag/'),
					        xsrfHeaderName: "X-CSRFToken",
					        xsrfCookieName: csrf,
				            headers: {
				            	'Content-type': 'application/json',
				            	"X-CSRFToken": csrf,
				            },
				            params: params
					    }
					    startProgress($("#ys-progress"));
						$http(config).then(function(retObj) {
							LoadAPIs(retObj.data.swagobj);
						}, function(retObj) {
							stopProgress($("#ys-progress"));
						});
	            	},
	            	"Cancel": function () {
	            		$(this).dialog("close");
	            		return;
	            	},
	            }
	        })
	        .html('<pre>')
	        .append('If this is a large module it could take\n',
	        	    'several minutes to generate the APIs.\n',
	        	    'You may want to consider choosing a branch\n',
	        	    'of the module and only generate those APIs.</pre>')
	        .dialog("open");
		} else {
			let config = {
				method: "GET",
		        url: $sce.trustAsResourceUrl('/restconf/genswag/'),
		        xsrfHeaderName: "X-CSRFToken",
		        xsrfCookieName: csrf,
	            headers: {
	            	'Content-type': 'application/json',
	            	"X-CSRFToken": csrf,
	            },
	            params: params
		    }
		    startProgress($("#ys-progress"));
			$http(config).then(function(retObj) {
				LoadAPIs(retObj.data.swagobj);
			}, function(retObj) {
				stopProgress($("#ys-progress"));
			});
		}
	}
});
