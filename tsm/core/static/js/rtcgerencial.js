/**
 * Controller para uso do angularjs na área rtc gerencial
 *
 * @author Jair Verçosa
 * @date 30/06/2014
 */


//Aplicação front-end rtc gerencial
var viewOppApp = angular.module('viewRtcApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('ngViewRtcCtrl', function ngViewRtcCtrl($scope, $http){
    
    /*
     * @var array dados do relatório
     */
    $scope.dataReport = null;

    /*
     * @var array cabeçalho
     */
    $scope.header = [];

    /*
     * @var int página atual
     */
    $scope.currentPage = 1;

    /**
     * 
     * Função para resgatar dados
     *
     * @return json
     */
    $scope.fnReload = function(){
        if($scope.dataReport != null){
            var ele = $('.table-rtc').parent();
            $scope.dataReport.fnDestroy();
            $(ele).html('');
            $(ele).append(
                '<table cellpadding="0" cellspacing="0" border="0" \
                        class="table table-bordered table-striped id="gridlist" \
                        url-data-source=""> \
                    <thead><tr class="custom-head"></tr></thead> \
                    <tbody></tbody> \
                    <tfoot></tfoot> \
                </table>'
            );
        }

        var optionsDataTable = {
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": '/relatorio/oportunidade/rtcgerencial/data/',
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
            "sDom": "<'table-rtc'<'row'<'col-lg-6'l>><'row'<'col-lg-12't>><'row table-footer'<'col-lg-6'i><'col-lg-6'p>>",
            "sPaginationType": "full_numbers",
            "scrollY": "550px",
            "scrollX": "100%",
            "scrollCollapse": true,
            "fnCreatedRow" : function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
                var elements = $(nRow).find('td');

                $.each(aData,function(i,obj){
                    if(typeof obj == 'object'){
                        var ele = $(nRow).find('td')[i];
                        html = '<ul class="ul-item-rtc-gerencial">';
                        $.each(obj,function(x,item){
                            html += '<li><a href="javascript:;" event="'+item.id+'" class="event-click">'+item.descricao+'</a></li>';
                        });
                        html += '</ul>';

                        $(ele).html(html);
                        $(ele).find('a').bind('click',$scope.onClickEvent);
                    }
                });
            },
            "fnServerParams": function ( aoData ) {
                aoData.push( { "name": 'start', "value": $('#id_periodo_ini').val() } );
                aoData.push( { "name": 'end', "value": $('#id_periodo_fim').val() } );
            }
        }

        $scope.loadHeader(function(){
            $scope.dataReport = $('#gridlist').dataTable(optionsDataTable);
            new $.fn.dataTable.FixedColumns($scope.dataReport);

            $('.table-rtc select').addClass('form-control');
            //$('.dataTables_length').parent().parent().append($('#id_cod_btn_report').html())
            //$('#btnPrint').bind('click',$scope.onClickPrint);
        });
    };

    /**
     * Evento que carrega cabeçalho da tabela de acordo com período
     * selecionado nos filtros do relatório
     *
     * @return void
     */
    $scope.loadHeader = function(fnAfterGet){
        $.ajax({
            url: '/relatorio/oportunidade/rtcgerencial/header/',
            data: {
                start: $('#id_periodo_ini').val(),
                end: $('#id_periodo_fim').val()
            },
            success: function(response){
                $scope.remakeHeader(response);
                if(typeof fnAfterGet == 'function'){
                    fnAfterGet(response);
                }
            },
            error: function(response){
                alert('Falha na carga do cabeçalho. Favor tentar novamente.');
                console.log(response.responseText);
            }
        });
    };

    /**
     * Refaz o cabeçalho da tabela
     *
     * @return void
     */
    $scope.remakeHeader = function(response){
        $scope.header = response.header;

        $('#gridlist thead tr').html('');
        $('#gridlist thead tr').append('<th>Oportunidade</th>');
        $.each($scope.header,function(i,obj){
            $('#gridlist thead tr').append('<th>'+obj+'</th>');
        });
    };

    /**
     * Evento de clique do botão buscar
     *
     * @return void
     */
    $scope.onClickBuscar = function(){
        $scope.fnReload();
    };

    /**
     * Evento de clique do botão imprimir
     *
     * @return void
     */
    $scope.onClickPrint = function(){
        //http://127.0.0.1:8082/relatorio/oportunidade/rtcgerencial/data/?iDisplayLength=5000&start=01%2F06%2F2014&end=08%2F07%2F2014
    };

    /**
     * Evento de clique do botão exportar para excel
     *
     * @return void
     */
    $scope.onClickExcel = function(){

    };

    /**
     * Evento de clique em um evento do rtc
     *
     * @return void
     */
    $scope.onClickEvent = function(){
        $.get(
            '/oportunidade/rtc/evento/'+$(this).attr('event')+'/',
            function(response){
                $('#mdl_event').html(response);
                $('#mdl_event').modal();
            }
        );
    };

    //Execuções iniciais
    $(".dateField").datepicker(app.datePickerBr);
    $scope.fnReload();
});

/*
 * Ajuste para paginação
 */
if ( $.fn.dataTable.Api ) {
    $.fn.dataTable.defaults.renderer = 'bootstrap';
    $.fn.dataTable.ext.renderer.pageButton.bootstrap = function ( settings, host, idx, buttons, page, pages ) {
        var api = new $.fn.dataTable.Api( settings );
        var classes = settings.oClasses;
        var lang = settings.oLanguage.oPaginate;
        var btnDisplay, btnClass;

        var attach = function( container, buttons ) {
            var i, ien, node, button;
            var clickHandler = function ( e ) {
                e.preventDefault();
                if ( e.data.action !== 'ellipsis' ) {
                    api.page( e.data.action ).draw( false );
                }
            };

            for ( i=0, ien=buttons.length ; i<ien ; i++ ) {
                button = buttons[i];

                if ( $.isArray( button ) ) {
                    attach( container, button );
                }
                else {
                    btnDisplay = '';
                    btnClass = '';

                    switch ( button ) {
                        case 'ellipsis':
                            btnDisplay = '&hellip;';
                            btnClass = 'disabled';
                            break;

                        case 'first':
                            btnDisplay = lang.sFirst;
                            btnClass = button + (page > 0 ?
                                '' : ' disabled');
                            break;

                        case 'previous':
                            btnDisplay = lang.sPrevious;
                            btnClass = button + (page > 0 ?
                                '' : ' disabled');
                            break;

                        case 'next':
                            btnDisplay = lang.sNext;
                            btnClass = button + (page < pages-1 ?
                                '' : ' disabled');
                            break;

                        case 'last':
                            btnDisplay = lang.sLast;
                            btnClass = button + (page < pages-1 ?
                                '' : ' disabled');
                            break;

                        default:
                            btnDisplay = button + 1;
                            btnClass = page === button ?
                                'active' : '';
                            break;
                    }

                    if ( btnDisplay ) {
                        node = $('<li>', {
                                'class': classes.sPageButton+' '+btnClass,
                                'aria-controls': settings.sTableId,
                                'tabindex': settings.iTabIndex,
                                'id': idx === 0 && typeof button === 'string' ?
                                    settings.sTableId +'_'+ button :
                                    null
                            } )
                            .append( $('<a>', {
                                    'href': '#'
                                } )
                                .html( btnDisplay )
                            )
                            .appendTo( container );

                        settings.oApi._fnBindAction(
                            node, {action: button}, clickHandler
                        );
                    }
                }
            }
        };

        attach(
            $(host).empty().html('<ul class="pagination"/>').children('ul'),
            buttons
        );
    }
}