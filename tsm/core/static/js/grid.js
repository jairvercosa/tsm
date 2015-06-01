/**
 * objeto para controle do grid
 *
 */
var grid = {
    /**
     * Url para pegar os dados do grid
     *
     * @var string urlData
     */
    urlData : '',
    /**
     * Url para deletar um registro
     *
     * @var string urlDel
     */
    urlDel : '',
    /**
     * id Atual que está sendo manupulado
     *
     * @var string currId
     */
    currId : '',
    /**
     * id do elemento da caixa de mensagem
     *
     * @var string msgElementId
     */
    msgElementId : '#mdlMsg_TSM',
    /**
     * token para post do delete
     *
     * @var string urlDel
     */
    csrfToken : '',
    /**
     * Objeto do datatable
     *
     * @var datatable obj
     */
    obj : null,
    /**
     * id da table do grid
     *
     * @var string tableObj
     */
    tableObj : '',
    /**
     * Função para retornar colunas não ordenáveis
     *
     * @return Array
     */
    fnGetDontSort : function(){
        var dontSort = [];
        $(grid.tableObj+' thead th').each( function () {
            if ( $(this).hasClass( 'no_sort' )) {
                dontSort.push( { "bSortable": false } );
            } else {
                dontSort.push( null );
            }
        });
        return dontSort;
    },
    /**
     * Função para click do botão excluir
     *
     * @return boolean
     */
    fnOnClickDel: function(typeCall){
        if(typeof typeCall == 'undefined') typeCall = 0;

        switch(typeCall){
            case 1:
                  var url_del = grid.urlDel + grid.currId;
                $.ajax({
                    type: 'post',
                    data: {'csrfmiddlewaretoken': grid.csrfToken },
                    url: url_del,
                    success: function(response){
                        grid.obj.fnDraw();
                        grid.fnOnClickDel(2);
                    },
                    error: function(response){
                        var result = $.parseJSON(response.responseText);

                        if(typeof result.message == 'undefined'){
                            alert('Infelizmente ocorreu um problema na tentativa de exclusão. Por favor entre em contato com o administrador do sistema');
                            console.log(response);
                        }else{
                            $(grid.msgElementId).modal('hide')
                            app.msgboxInfo('Acesso negado',result.message);
                        }
                    }
                });        
                  break;
            case 2:
                  $(grid.msgElementId).modal('hide')
                  break;
        default:
            grid.currId = $(this).attr('alt')+'/';
            $(grid.msgElementId).modal();
        }
    },
    /**
     * Função para instanciar o objeto
     *
     * @return boolean
     */
    fnStartObject : function(option){
        var dontSort = grid.fnGetDontSort();
        grid.urlData = option.urlData;
        grid.urlDel = option.urlDel;
        grid.tableObj = option.tableObj;

        if(typeof option.btnPrint == 'undefined')
            option.btnPrint = true;

        if(typeof option.aaSorting == 'undefined')
            option.aaSorting = [[0,""]]

        if(typeof option.fnCreatedRow == 'undefined')
            option.fnCreatedRow = function(){ return true; }

        if(typeof option.fnDrawCallback == 'undefined'){
            option.fnDrawCallback = function(oSettings){
                $(oSettings.nTable).find('tr').addClass('tr-selectable');
                $('.tr-selectable').bind('dblclick',grid.onDblClick);
            }
        }

        if(typeof option.fnServerParams == 'undefined')
            option.fnServerParams = function(){return true;}

        if(typeof option.fnFooterCallback == 'undefined')
            option.fnFooterCallback = null;

        if(typeof option.tableTools == 'undefined')
            option.tableTools = {
                //"sSwfPath": "/static/swf/copy_csv_xls_pdf.swf",
                "aButtons": [
                    {
                        "sExtends": "print",
                        "oSelectorOpts": { filter: 'applied', order: 'current' },
                        "sButtonText": "Visualizar",
                        "sInfo": "<h6>Visualização de Impressão</h6><p>Por favor, use a função de impressão do seu Browser para "+
                                 "imprimir os dados. Pressione Esc para finalizar.</p>",
                        "sToolTip": "Visualizar impressão",
                        "fnComplete": function(){ $('.modal').hide(); }
                    }
                    
                ]
            }

        var optionsDataTable = {
            "aoColumns": dontSort,
            "bProcessing": true,
            "bServerSide": true,
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
            "sDom": "<'row'<'col-lg-2 col-xs-5'l><'col-lg-4 btn-list'><'col-lg-6'<'pull-right'f>>r><'row'<'col-lg-12't>><'row'<'col-lg-6 col-xs-4'i><'col-lg-6'p>>",
            "sPaginationType": "full_numbers",
            "aaSorting": option.aaSorting,
            "fnCreatedRow": option.fnCreatedRow,
            "fnDrawCallback": option.fnDrawCallback,
            "fnServerParams": option.fnServerParams,
            "fnFooterCallback": option.fnFooterCallback,
            "bDestroy": true,
        }

        grid.obj = $(grid.tableObj).dataTable(optionsDataTable);
        var tt = new $.fn.dataTable.TableTools(grid.obj, option.tableTools);
        $(tt.fnContainer()).appendTo('div.btn-list');
        $('.DTTT_button_print').prepend('<i class="icon icon-white icon-print"></i>')
        //$('.DTTT_button_pdf').prepend('<i class="icon icon-white icon-file"></i>')

        $('.dataTables_wrapper input').addClass('form-control');
        $('.dataTables_wrapper select').addClass('form-control');
        
        grid.csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $('.btnDel').live('click',grid.fnOnClickDel);
        
        $('#btnConfirmDel').bind('click',function(){
            grid.fnOnClickDel(1);
        });

        $.extend( $.fn.dataTableExt.oStdClasses, {
            "sWrapper": "dataTables_wrapper form-inline"
        });
    },

    /**
     * Evento de duplo clique da linha do grid
     *
     * @return void
     */
    onDblClick: function() {
        if($(this).find('.btnEdit').length > 0)
            window.location = $(this).find('.btnEdit').attr('href');
    },
}