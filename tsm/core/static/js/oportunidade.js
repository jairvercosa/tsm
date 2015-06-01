/**
 * Controller para uso do angularjs na área de visão gerencial
 *
 * @author Jair Verçosa
 * @date 30/04/2014
 */


//Aplicação front-end oportunidade
var viewOppApp = angular.module('viewOppApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('ngViewOppCtrl', function ngViewOppCtrl($scope, $http){
    /*
     * @var array dataChartsTop - Valores dos gráficos
     */
    $scope.dataChartsTop = [];
    
    /*
     * @var array asInitVals - Variável padrão para receber valores de pesquisa dos campos
     * no rodapé
     */
    $scope.asInitVals = [];

    /*
     * @var array dataToCharts - Dados para os gráficos
     */
    $scope.dataToCharts = [];

    /*
     * Gera os gráficos
     */
    $scope.makeChartsTop = function(){
        //Gross
        var dataGross = [];
        var ticks = [];
        var labels = [];

        for (var i = 0; i < $scope.dataChartsTop.gross.items.length; i++) {
            ticks.push($scope.dataChartsTop.gross.items[i].title);
            dataGross.push([i+1,$scope.dataChartsTop.gross.items[i].value]);
        };
        
        var chartGross = $.jqplot('id_chart_gross',[dataGross],{
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawGridlines: false,
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#0c72b0","#a2bf2f"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {
                    animation: {
                        speed: 2200
                    },
                    barWidth: 35,
                    barMargin: 0,
                    highlightMouseOver: false,
                    shadowDepth: 2
                },
                pointLabels: { show: true, location: 'n', edgeTolerance: -15 ,formatString: '%.2f', formatter: $.jqplot.realFormatter}
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                },
                yaxis: {
                    show: false,
                    showTicks: false,
                    showTickMarks: false
                }
            }
        });

        //Ponderado
        var dataPonderado = [];
        ticks = [];
        labels = [];

        for (var i = 0; i < $scope.dataChartsTop.ponderado.items.length; i++) {
            ticks.push($scope.dataChartsTop.ponderado.items[i].name);
            dataPonderado.push([$scope.dataChartsTop.ponderado.items[i].value,i+1]);
        };

        var chartPonderado = $.jqplot('id_chart_ponderado',[dataPonderado],{
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawGridlines: false,
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#0c72b0","#a2bf2f","#EAA228", "#579575", "#839557", "#958c12", "#953579", "#4b5de4", "#d8b83f", "#ff5800", "#0085cc"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                yaxis: 'yaxis',
                rendererOptions: {
                    animation: {
                        speed: 2200
                    },
                    barWidth: 10,
                    barMargin: 0,
                    highlightMouseOver: false,
                    fillToZero: true,
                    shadowDepth: 2,
                    barDirection: 'horizontal',
                    varyBarColor: true
                },
                pointLabels: { show: true, location: 'e', edgeTolerance: -45, formatString: '%.2f', formatter: $.jqplot.realFormatter },
            },
            axes: {
                xaxis: {
                    pad: '0',
                    show: false,
                    showTicks: false,
                    showTickMarks: false
                },
                yaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                }
            },
        });

        //P/U
        var dataSituacao = [];
        ticks = [];
        labels = [];

        for (var i = 0; i < $scope.dataChartsTop.situacao.items.length; i++) {
            ticks.push($scope.dataChartsTop.situacao.items[i].name);
            
            var valores = [];
            for (var j = 0; j < $scope.dataChartsTop.situacao.items[i].situacoes.length; j++) {
                valores.push($scope.dataChartsTop.situacao.items[i].situacoes[j].value);

                var match = false;
                $.each(labels,function(a,b){
                    if($scope.dataChartsTop.situacao.items[i].situacoes[j].name == b.label){
                        match = true;
                    }    
                })

                if(!match){
                    labels.push({'label' : $scope.dataChartsTop.situacao.items[i].situacoes[j].name});
                }
                
            };

            $.each(valores,function(y,obj){
                if(y>(dataSituacao.length-1)){ //Se nao houver o item
                    dataSituacao.push([obj]);
                }else{
                    dataSituacao[y].push(obj);
                }
            })
        };
        
        var chartSituacao = $.jqplot('id_chart_situacao',dataSituacao,{
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawGridlines: false,
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#d8b83f","#a2bf2f","#EAA228", "#579575", "#839557", "#958c12", "#953579", "#4b5de4", "#d8b83f", "#ff5800", "#0085cc"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                yaxis: 'yaxis',
                rendererOptions: {
                    animation: {
                        speed: 2200
                    },
                    barWidth: 25,
                    barMargin: 0,
                    highlightMouseOver: false,
                    fillToZero: true,
                    shadowDepth: 2
                },
                pointLabels: { show: true, location: 'n', edgeTolerance: -15, formatString: '%.2f', formatter: $.jqplot.realFormatter}
            },
            series:labels,
            legend: { show: true }, 
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                },
                yaxis: {
                    show: false,
                    showTicks: false,
                    showTickMarks: false
                }
            }
        });

        //Fator
        var dataFator = [];
        ticks = [];
        labels = [];

        for (var i = 0; i < $scope.dataChartsTop.fator.items.length; i++) {
            ticks.push($scope.dataChartsTop.fator.items[i].name);
            dataFator.push([i+1,$scope.dataChartsTop.fator.items[i].value]);
        };
        
        var chartFator = $.jqplot('id_chart_fator',[dataFator],{
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawGridlines: false,
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#0c72b0","#a2bf2f","#EAA228", "#579575", "#839557", "#958c12", "#953579", "#4b5de4", "#d8b83f", "#ff5800", "#0085cc"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                yaxis: 'yaxis',
                rendererOptions: {
                    animation: {
                        speed: 2200
                    },
                    barWidth: 35,
                    barMargin: 0,
                    highlightMouseOver: true,
                    fillToZero: true,
                    shadowDepth: 2,
                    varyBarColor: true
                },
                pointLabels: { show: true, location: 'n', edgeTolerance: -15, formatString: '%.2f', formatter: $.jqplot.realFormatter }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                },
                yaxis: {
                    pad: '0',
                    show: false,
                    showTicks: false,
                    showTickMarks: false
                }
            },
        });
    };

    /*
     * Gera os gráficos do lado direito
     */
    $scope.makeChartsRight = function(data){
        //Oportunidade/Filial
        /*$('#id_chart_filial').html('');
        var dados = [[data.values.oportunidade],[100-data.values.oportunidade]];
        var chart_filial = $.jqplot('id_chart_filial',dados,{
            stackSeries: true,
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                shadow: false,
            },
            seriesColors:["#8aa22b","#0c72b0"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                rendererOptions: {
                    animation: { speed: 1000 },
                    barWidth: 70,
                    barMargin: 30,
                    highlightMouseOver: true,
                    shadowDepth: 2
                },
                pointLabels: {
                    show: true, 
                    location:'n', 
                    formatString: '%.2f %',
                    ypadding: 120
                }
            },
            series: [{label: 'Oportunidade' },{label: 'Filial'}],
            legend: { show: true, location: 'e', placement: 'outside' }, 
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                },
                yaxis: {
                    padMin: 0
                }
            },
        });*/

        //Responsável
        $('#id_chart_responsavel').html('');
        //Se valor zerado, significa que está sem meta então o total deve ser 100
        if(data.values.responsavel==0) data.values.responsavel = 100
        var dadosResponsavel = [[data.values.responsavel],[100-data.values.responsavel]];
        var chart_responsavel = $.jqplot('id_chart_responsavel',dadosResponsavel,{
            stackSeries: true,
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#8aa22b","#0c72b0"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                rendererOptions: {
                    animation: { speed: 1000 },
                    barWidth: 40,
                    barMargin: 30,
                    highlightMouseOver: true,
                    shadowDepth: 2
                },
                pointLabels: {
                    show: false, 
                }
            },
            series: [{label: 'Oportunidade' }, {label: 'Meta'}],
            legend: { show: true, location: 'e', placement: 'outside' }, 
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                },
                yaxis: {
                    //padMin: 0,
                    tickOptions: {formatString: '%.2f %'}
                }
            },
        });

        //Líder
        $('#id_chart_lider').html('');
        //Se valor zerado, significa que está sem meta então o total deve ser 100
        if(data.values.lider==0) data.values.lider = 100
        var dadosLider = [[data.values.lider],[100-data.values.lider]];
        var chart_lider = $.jqplot('id_chart_lider',dadosLider,{
            stackSeries: true,
            animate: true,
            animateReplot: true,
            grid: {
                background : 'transparent',
                drawBorder: false,
                shadow: false,
            },
            seriesColors:["#8aa22b","#0c72b0"],
            seriesDefaults:{
                renderer: $.jqplot.BarRenderer,
                showHighlight: false,
                rendererOptions: {
                    animation: { speed: 1000 },
                    barWidth: 40,
                    barMargin: 30,
                    highlightMouseOver: true,
                    shadowDepth: 2
                },
                pointLabels: {
                    show: false, 
                }
            },
            series: [{label: 'Oportunidade' },{label: 'Meta'}],
            legend: { show: true, location: 'e', placement: 'outside' }, 
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                },
                yaxis: {
                    padMin: 0,
                    tickOptions: {formatString: '%.2f %'}
                }
            },
        });
    };

    /*
     * Evento click da linha da tabela
     */
    $scope.onSelectRow = function(aData){
        var posId = 11;
        var oportunidade_id = 0;
        var match = false;
        var data = {};

        $('.row_selected').removeClass('row_selected');
        $(this).addClass('row_selected');
        
        //Pega os dados do grid e a posição selecionada
        var data = grid.obj.fnGetData();
        var idx = grid.obj.$('.row_selected').index();
        
        if(idx >= 0){
            oportunidade_id = data[idx][posId];

            $.each($scope.dataToCharts,function(i,obj){
                if(obj.oportunidade == oportunidade_id){
                    data = obj;
                    match = true;
                    return false;
                }
            });

            if(!match){
                $.ajax({
                    type: 'GET',
                    url : '/oportunidade/visaogerencial/indicadores/'+oportunidade_id+'/',
                    success: function(response){
                        data = response.data;
                        $scope.dataToCharts.push(data);
                        $scope.updateCharts(data);
                    },
                    error: function(response){ console.log(response.responseText); }
                });
            }else{
                $scope.updateCharts(data);
            }
        }else{
            $('#id_chart_filial, #id_chart_responsavel, #id_chart_lider').fadeOut('fast');
        }
    };

    /*
     * Atualiza os charts da barra lateral da tela
     */
    $scope.updateCharts = function(data){
        $scope.makeChartsRight(data);
    };

    /*
     * Refatoração da função de geração da datatable
     */
    grid.fnStartObject = function(option){
        var dontSort = grid.fnGetDontSort();
        grid.urlData = option.urlData;
        grid.urlDel = option.urlDel;
        grid.tableObj = option.tableObj;

        grid.obj = $(grid.tableObj).dataTable({
            "aoColumns": dontSort,
            "bProcessing": true,
            "bServerSide": false,
            "sAjaxSource": grid.urlData,
             "oLanguage": {
                 "oPaginate" : {
                     "sFirst" : "<<",
                     "sLast" : ">>",
                     "sPrevious" : "<",
                     "sNext" : ">",
                 },
                 "sProcessing" : "Processando",
                 "sSearch": "Pesquisar",
                "sLengthMenu": "_MENU_ registros por página",
                "sZeroRecords": "Nenhum registro encontrado",
                "sInfo": "Exibindo _START_ até _END_ de _TOTAL_ registros",
                "sInfoEmpty": "Exibindo 0 até 0 de 0 registros",
                "sInfoFiltered": "(Filtrado de _MAX_ total registros)"
            },
            "sDom": "<'row'<'col-lg-6'l><'col-lg-6'<'pull-right'f>>r><'row'<'col-lg-12't>><'row'<'col-lg-6'i><'col-lg-6'p>>",
            "sPaginationType": "full_numbers",
            "aaSorting": option.aaSorting,
            "fnCreatedRow" : function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
                $(nRow).bind('click',$scope.onSelectRow);

                var ele = $(nRow).find('td')[5];
                var text = $(ele).html();
                var content = "<ul>";
                $.each(aData[10],function(i,obj){
                    var idx = i+1
                    content += "<li>"+idx+".<strong> "+obj.pergunta+"</strong> <span>"+obj.resposta+"</span></li>";
                });
                content += "</ul>";

                $(ele).html('<a class="link-questions" href="javascript:void(0)" data-toggle="popover" title data-content="'+content+'" role="a" data-original-title="Perguntas">'+text+'</a>');

                $(ele).find('a').popover({
                    trigger: 'hover',
                    html : true
                });
            }
        });
        
        //Inputs de pesquisa no rodapé
        $("tfoot input").keyup(function (){ grid.obj.fnFilter(this.value, $("tfoot input").index(this));});
        $("tfoot input").each(function (i) {$scope.asInitVals[i] = this.value;});
        $("tfoot input").focus( function () {
            if ( this.className == "search_init" ){
                this.className = "";
                this.value = "";
            }
        });
         
        $("tfoot input").blur( function (i) {
            if ( this.value == "" ){
                this.className = "search_init";
                this.value = $scope.asInitVals[$("tfoot input").index(this)];
            }
        });

        $('.dataTables_wrapper input').addClass('form-control');
        $('.dataTables_wrapper select').addClass('form-control');
        
        grid.csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $.extend( $.fn.dataTableExt.oStdClasses, {
            "sWrapper": "dataTables_wrapper form-inline"
        });
    };

    $.ajax({
        type: 'GET',
        url : '/oportunidade/visaogerencial/indicadorestop/',
        success: function(response){
            $scope.dataChartsTop = response.data;
            $scope.$apply();
            $('#span-total-gross').fadeIn();
            $('#span-total-ponderado').fadeIn();
            $('#span-total-situacao').fadeIn();
            $('#span-total-fator').fadeIn();
            $scope.makeChartsTop();
        },
        error: function(response){ console.log(response.responseText); }
    });
});