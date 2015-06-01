/**
 * Arquivo para manipulação da lista de oportunidades
 *
 * @author Jair Verçosa
 * @date 27/05/2014
 */
var oportunidade = {
    /*
     * @var array - Guarda valores iniciais para filtros
     */
    asInitVals : [],

    /*
     * Valores do registro que está editando
     */
    rowEditing: {},

    /**
     * Para ser executada ao carregar a página
     *
     * @return void
     */
    onReady : function(){

        //Chamada do datatable
        oportunidade.fnLoadTable();

        //Caminho customizado para formulário de criação
        $('#btnAddList').unbind('click'); 
        $('#btnAddList').bind('click',function(){ 
            window.location.href = '/oportunidade/formulario/' 
        });

        $('#btnSearch').bind('click',oportunidade.onClickBtnSearch);
        $('.btnEditFast').live('click',oportunidade.onClickEditFast);
        $('.chkMW').live('change',oportunidade.onClickCheckMW);
        $('.chkBC').live('change',oportunidade.onClickCheckBC);
        
        $('tfoot').find('.search_init').on('focus',oportunidade.showFilterDataForm);
        $('tfoot').find('button').on('focus',oportunidade.showFilterDataForm);
        
        $('.div-form-date').find('input[type=text]').on('change',oportunidade.onChangeDataForm);
        $('.div-form-date').find('input[type=text]').datepicker(app.datePickerBr);
        $('html').click(function(event){
            if(typeof $(event.target).parent().attr('class') != 'undefined')
                if($(event.target).parent().attr('class').indexOf("datepicker") < 0 && $('.div-form-date').find(event.target).length == 0) {
                    oportunidade.hideDataForm(event);
                }
        });

        oportunidade.makeSelectFieldsSearch();
        $('.checkinput').bind('click',oportunidade.onClickCheckMultSelect);
    },

    /**
     * Exibe formulário para seleção da data de previsão de fechamento no
     * filtro da listagem de oportunidades
     *
     * @return void
     */
    showFilterDataForm: function(event){
        event.stopPropagation();
        var ele_dtfechamento = $(this);

        if($(ele_dtfechamento).attr('name') != 'dtfechamento'){
            oportunidade.hideDataForm(event);
        }else{
            $('.div-form-date').css({
                'top': $(ele_dtfechamento).offset().top + $(ele_dtfechamento).outerHeight(),
                'right': $(window).width() - ($(ele_dtfechamento).offset().left + $(ele_dtfechamento).outerWidth()),
                'z-index': 1000
            });
            $('.div-form-date').fadeIn('fast');
        }
    },

    /**
     * Retorna todos membros que o usuário pode ver
     *
     * @return void
     */
    makeSelectFieldsSearch: function(){
        $('tfoot').find('.ajaxLoading').show();
        $.ajax({
            'url': '/equipe/membro/getchild/',
            'success': function(response){
                $('tfoot').find('.ajaxLoading').hide();
                var selects = $('tfoot').find('.select-members');
                $.each(selects,function(i,obj){
                    $(obj).show();
                    $.each(response,function(x,item){
                        $(obj).append('<option value="'+item.id+'">'+item.nome+'</oportunidade>');
                    });
                });
            },
            'error':function(){
                $('tfoot').find('.ajaxLoading').hide();
            }
        });
    },

    /**
     * Esconde formulario de data de previsão
     *
     * @return void
     */
    hideDataForm: function(event){
        $('.div-form-date').fadeOut('fast');
    },

    /**
     * Altera data de previsao
     *
     * @return void
     */
    onChangeDataForm: function(){
        var elements = $('.div-form-date').find('input[type=text]');
        var result = '';
        
        result = $(elements[0]).val();
        result += ':' + $(elements[1]).val();

        $('tfoot').find('input[name=dtfechamento]').val(result);
    },
    /**
     * Carrega table
     *
     * @return void
     */
    fnLoadTable : function(){
        
        //PreFiltro
        if(typeof preFilter != 'undefined'){
            //filtro de temperaturas
            $('#id-ul-temp li').find('.checkinput').removeClass('icon-checked');
            $('#id-ul-temp li').find('.checkinput').addClass('icon-unchecked');
            $.each($('#id-ul-temp li').find('.checkinput'),function(i,obj){
                $.each(preFilter.tipotemperatura,function(x,item){
                    if($(obj).attr('alt')==item){
                        $(obj).removeClass('icon-unchecked');
                        $(obj).addClass('icon-checked');
                    }
                });
            });

            //filtro de receitas
            $('#id-ul-receita li').find('.checkinput').removeClass('icon-checked');
            $('#id-ul-receita li').find('.checkinput').addClass('icon-unchecked');
            $.each($('#id-ul-receita li').find('.checkinput'),function(i,obj){
                $.each(preFilter.receitas,function(x,item){
                    if($(obj).attr('alt')==item){
                        $(obj).removeClass('icon-unchecked');
                        $(obj).addClass('icon-checked');
                    }
                });
            });

            //filtro de receitas
            $('input[name=dtfechamento]').val(preFilter.dtFechamento);
        }

        //Chamada do datatable
        grid.fnStartObject({
            'urlData' : "/oportunidade/lista/data/",
            'urlDel'  : '/oportunidade/remove/',
            'tableObj': '#gridlist',
            'aaSorting': [[10,'desc']],
            "fnCreatedRow" : function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
                var ele = $(nRow).find('td')[6];
                var text = $(ele).html();
                var content = "<ul>";
                $.each(aData[15],function(i,obj){
                    var idx = i+1
                    content += "<li>"+idx+".<strong> "+obj.pergunta+"</strong> <span>"+obj.resposta+"</span></li>";
                });
                content += "</ul>";

                $(ele).html('<a class="link-questions" href="javascript:void(0)" data-toggle="popover" title data-content="'+content+'" role="a" data-original-title="Perguntas">'+text+'</a>');

                $(ele).find('a').popover({
                    trigger: 'hover',
                    html : true
                });

                //Rtc
                var eleRtc = $(nRow).find('td')[11]
                var respRtc = $(eleRtc).html();
                
                $(eleRtc).html('<a href="/oportunidade/lista/'+aData[16]+'/rtc/">'+respRtc+'</a>');

                //MW e BC
                var eleMW = $(nRow).find('td')[12];
                var eleBC = $(nRow).find('td')[13];
                
                if(canChangeMWBC){
                    var checkedMW = (aData[12]) ? 'checked="checked"' : '';
                    var checkedBC = (aData[13]) ? 'checked="checked"' : '';
                    $(eleMW).html('<input class="chkMW" type="checkbox" name="checkMW" alt="'+aData[16]+'" '+checkedMW+'/>');
                    $(eleBC).html('<input class="chkBC" type="checkbox" name="checkBC" alt="'+aData[16]+'" '+checkedBC+'/>');

                }else{
                    var checkedMW = (aData[12]) ? 'Sim' : 'Não';
                    var checkedBC = (aData[13]) ? 'Sim' : 'Não';
                    $(eleMW).html(checkedMW);
                    $(eleBC).html(checkedBC);
                }

                if(aData[12]) $(eleMW).parent().find('td').addClass('mustwinline-table');
                

                //Ajustes para responsivo
                $($(nRow).find('td')[1]).addClass('hidden-xs');
                $($(nRow).find('td')[2]).addClass('hidden-xs');
                $($(nRow).find('td')[3]).addClass('hidden-xs');
                //$($(nRow).find('td')[4]).addClass('hidden-xs');
                $($(nRow).find('td')[5]).addClass('hidden-xs hidden-sm');
                $($(nRow).find('td')[6]).addClass('hidden-xs hidden-sm hidden-md');
                $($(nRow).find('td')[7]).addClass('hidden-xs');
                //$($(nRow).find('td')[8]).addClass('hidden-xs');
                $($(nRow).find('td')[9]).addClass('hidden-xs hidden-sm');
                //$($(nRow).find('td')[10]).addClass('hidden-xs');
                $($(nRow).find('td')[11]).addClass('hidden-xs');
                $($(nRow).find('td')[12]).addClass('hidden-xs');
                $($(nRow).find('td')[13]).addClass('hidden-xs');
            },
            "fnServerParams": function ( aoData ) {
                $.each($('tfoot .search_init'),function(i,ele){
                    aoData.push( { "name": $(ele).attr('name'), "value": $(ele).val() } );
                });

                //Monta busca de receitas
                var receitas = '';
                $.each($('#id-ul-receita li').find('.icon-checked'),function(i,obj){
                    receitas += $(obj).html() + '+';
                });
                aoData.push( { "name": "receita", "value": receitas.substr(0,receitas.length-1) } );

                //Monta busca de situações
                var situacoes = '';
                $.each($('#id-ul-situacao li').find('.icon-checked'),function(i,obj){
                    situacoes += $(obj).html() + '+';
                });
                aoData.push( { "name": "situacao", "value": situacoes.substr(0,situacoes.length-1) } );

                //Monta busca de temperaturas
                var temps = '';
                $.each($('#id-ul-temp li').find('.icon-checked'),function(i,obj){
                    temps += $(obj).html() + '+';
                });
                aoData.push( { "name": "tipotemperatura", "value": temps.substr(0,temps.length-1) } );

                //Monta busca de temperaturas automáticas
                var tempsAuto = '';
                $.each($('#id-ul-tempauto li').find('.icon-checked'),function(i,obj){
                    tempsAuto += $(obj).html() + '+';
                });
                aoData.push( { "name": "temperatura_auto", "value": tempsAuto.substr(0,tempsAuto.length-1) } );

                if(typeof preFilter != 'undefined'){
                    if(typeof preFilter.usufilter != 'undefined')
                        aoData.push( { "name": "userfilter", "value": preFilter.usufilter } );                    
                }

                if(typeof preFilter != 'undefined'){
                    aoData.push( { "name": "frdash", "value": 1} );                    
                }
            },
            "fnFooterCallback": function (row, data, start, end, display){
                var api = this.api();
                var intVal = function ( i ) {
                    return typeof i === 'string' ?
                        i.replace(/[\$,]/g, '')*1 :
                        typeof i === 'number' ?
                            i : 0;
                };

                // Total over all pages
                try{
                    returnFromServer = api.settings()[0].json
                    var total = returnFromServer.totalValor;
                    var totalPond = returnFromServer.totalPond;
                }catch(err){
                    var total = 0;
                    var totalPond = 0;
                }

                // Update footer
                $( api.column( 4 ).footer() ).html(
                    $.number(total,2)
                );
                $( api.column( 5 ).footer() ).html(
                    $.number(totalPond,2)
                );
            },
            "tableTools": {
                //"sSwfPath": "/static/swf/copy_csv_xls_pdf.swf",
                "aButtons": [
                    {
                        "sExtends": "print",
                        "oSelectorOpts": { filter: 'applied', order: 'current' },
                        "sButtonText": "Visualizar",
                        "sInfo": "<h6>Visualização de Impressão</h6><p>Por favor, use a função de impressão do seu Browser para "+
                                 "imprimir os dados. Pressione Esc para finalizar.</p>",
                        "sToolTip": "Visualizar impressão",
                        "fnClick": function ( nButton, oConfig ) {
                            $('.tr-filters-list').hide();
                            $('.div-form-date').hide();
                            this.fnPrint( true, oConfig );
                        },
                        "fnComplete": function(){ 
                            var that = this;
                            $(document).bind( "keydown.DTTT", function(e) {
                                /* Only interested in the escape key */
                                if ( e.keyCode == 27 )
                                {
                                    e.preventDefault();
                                    $('.tr-filters-list').show();
                                    that._fnPrintEnd.call( that, e );
                                }
                            } );
                            $('.modal').hide(); 
                        }
                    }
                    
                ]
            }
        });
    },

    /**
     * Evento de clique do botão pesquisar
     *
     * @return void
     */
    onClickBtnSearch: function(){
        grid.obj.fnDraw();
        $('#gridlist').css('width','100%');
    },

    /**
     * Evento de clique do botão de edição rápida 
     *
     * @return void
     */
    onClickEditFast : function(){
        oportunidade.onClickCancelForm();
        var eleRow = $(this).parent().parent().parent();

        $(eleRow).addClass('editing');

        var eleTipo   = $(eleRow).find('td')[1];
        var eleProd   = $(eleRow).find('td')[2];
        var eleStatus = $(eleRow).find('td')[3];
        var eleValor  = $(eleRow).find('td')[4];
        var elePond   = $(eleRow).find('td')[5];
        var eleTemp   = $(eleRow).find('td')[7];
        var eleData   = $(eleRow).find('td')[10];
        var eleMW     = $(eleRow).find('td')[12];
        var editFree  = true;

        //Verifica se o usuário pode editar todos os campos livremente
        if($(eleMW).find('input').length == 0){
            if($(eleMW).html()=='Sim'){
                editFree = false;
            }
        }

        oportunidade.rowEditing = {
            "id": $(this).attr('alt'),
            "receita": $(eleTipo).html(),
            "situacao": $(eleStatus).html(),
            "valor": $(eleValor).html(),
            "ponderado": $(elePond).html(),
            "tipotemperatura": $(eleTemp).html(),
            "dtFechamento": $(eleData).html(),
            "produto": $(eleProd).html(),
        }

        //Monta Campo de Tipo
        var inputField = '<select id="id_receita" name="receita" class="form-control">';
        //Pega variavel instanciada no html
        $.each(receita,function(i,obj){
            inputField += '<option value="'+obj.id+'" ';
            if(obj.nome==oportunidade.rowEditing.receita) inputField += 'selected="selected"';
            inputField += '>'+obj.nome+'</option>';
        });
        
        inputField += '</select>';
        $(eleTipo).html(inputField);

        //Monta Campo de produto
        var inputField = '<select id="id_produto" name="produto" class="form-control">';
        //Pega variavel instanciada no html
        $.each(produto,function(i,obj){
            inputField += '<option value="'+obj.id+'" ';
            if(obj.nome==oportunidade.rowEditing.produto) inputField += 'selected="selected"';
            inputField += ' data_resume_name="'+obj.nome+'">'+obj.nome+' - '+obj.fabricante+'</option>';
        });

        inputField += '</select>';
        $(eleProd).html(inputField);

        //Monta Campo de Situação
        var inputField = '<select id="id_situacao" name="situacao" class="form-control">';
        //Pega variavel instanciada no html
        $.each(situacao,function(i,obj){
            inputField += '<option value="'+obj.id+'" ';
            if(obj.nome==oportunidade.rowEditing.situacao) inputField += 'selected="selected"';
            inputField += '>'+obj.nome+'</option>';
        });

        inputField += '</select>';
        $(eleStatus).html(inputField);

        
        //Monta Campo de Temperatura
        var inputField = '<select id="id_tipotemperatura" name="tipotemperatura" class="form-control">';
        //Pega variavel instanciada no html
        $.each(tipotemperatura,function(i,obj){
            inputField += '<option value="'+obj.id+'" ';
            if(obj.nome==oportunidade.rowEditing.tipotemperatura) inputField += 'selected="selected"';
            inputField += '>'+obj.nome+'</option>';
        });

        inputField += '</select>';
        $(eleTemp).html(inputField);

        if(editFree){
            //Monta campo de valor e data
            $(eleValor).html('<input id="id_valor" name="valor" class="form-control" value="'+oportunidade.rowEditing.valor+'" />');
            $(eleData).html('<input id="id_dtFechamento" name="dtFechamento" class="form-control no-background" value="'+oportunidade.rowEditing.dtFechamento+'" />');

            $('#id_dtFechamento').datepicker(app.datePickerBr);
            $('#id_valor').number(true, 2);
        }

        $(this).parent().parent().css('position','relative');
        $(this).parent().parent().find('.action-buttons').hide();
        $(this).parent().parent().append(
            '<div class="div-group-btnfast"> \
                <button class="btn btn-sm btn-success" title="Salvar" id="btnSaveForm"><i class="icon icon-white icon-ok"></i></button> \
                <button class="btn btn-sm btn-default" title="Cancelar" id="btnCancelForm"><i class="icon icon-white icon-remove"></i></button> \
            </div>'
        );

        $('#btnSaveForm').bind('click',oportunidade.onClickSaveForm);
        $('#btnCancelForm').bind('click',oportunidade.onClickCancelForm);
    },

    /**
     * Evento de clique para botao salvar do form de edicao rapida
     *
     * @return void
     */
    onClickSaveForm: function(){
        $('#mdl_form_saving').modal();
        $('#mdl_form_saving').find('.modal-footer').hide();
        $('#mdl_form_saving').find('.ajaxLoading').parent().css('text-align','center');
        $('#mdl_form_saving').find('.ajaxLoading').fadeIn('fast');
        $('#modal_msg_error').empty();

        var dataToSave = oportunidade.rowEditing;
        if($('#id_receita').length>0) dataToSave.receita = $('#id_receita').val();
        if($('#id_situacao').length>0) dataToSave.situacao = $('#id_situacao').val();
        if($('#id_valor').length>0) dataToSave.valor = $('#id_valor').val();
        if($('#id_tipotemperatura').length>0) dataToSave.tipotemperatura = $('#id_tipotemperatura').val();
        if($('#id_dtFechamento').length>0) dataToSave.dtFechamento = $('#id_dtFechamento').val();
        if($('#id_produto').length>0) dataToSave.produto = $('#id_produto').val();
        
        
        $.ajax({
            url: '/oportunidade/lista/edicaorapida/'+oportunidade.rowEditing.id+'/',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'receita'        : dataToSave.receita,
                'situacao'       : dataToSave.situacao,
                'valor'          : dataToSave.valor.replace(',',''),
                'tipotemperatura': dataToSave.tipotemperatura,
                'dtFechamento'   : dataToSave.dtFechamento,
                'produto'        : dataToSave.produto,
                'edicaorapida'   : true
            },
            success: function(response){
                if(!response.success){
                    $('#mdl_form_saving').find('.modal-footer').show();
                    $('#mdl_form_saving').find('.ajaxLoading').hide();   
                    var message = response.message+ '<br /><br />';
                    
                    $('#modal_msg_error').html(message);
                }else{
                    $('#mdl_form_saving').modal('hide');
                    oportunidade.rowEditing = {
                        "id"             : response.data.id,
                        "receita"        : response.data.receita,
                        "situacao"       : response.data.situacao,
                        "valor"          : $.number(response.data.valor,2),
                        "ponderado"      : $.number(response.data.ponderado,2),
                        "tipotemperatura": response.data.tipotemperatura,
                        "dtFechamento"   : response.data.dtFechamento,
                        "produto"        : response.data.produto
                    }
                    grid.obj.fnDraw();
                    oportunidade.onClickCancelForm();
                }
            },
            error: function(response){
                $('#mdl_form_saving').find('.modal-footer').show();
                $('#mdl_form_saving').find('.ajaxLoading').hide();

                try{
                    result = $.parseJSON(response.responseText);
                    message = result.message+ '<br /><br />';
                    
                    $('#modal_msg_error').html(message);
                }catch(err){
                    console.log(response.responseText);
                }
            }
        });
        
    },

    /**
     * Evento para cancelar edição rápida
     *
     * @return void
     */
    onClickCancelForm: function(){
        var eleRow = $('.editing');

        if($(eleRow).length>0){
            $(eleRow).find('input').remove();
            $(eleRow).find('select').remove();
            $(eleRow).find('.div-group-btnfast').remove();
            $(eleRow).find('.action-buttons').show();

            var eleTipo   = $(eleRow).find('td')[1];
            $($(eleRow).find('td')[1]).html(oportunidade.rowEditing.receita);
            $($(eleRow).find('td')[2]).html(oportunidade.rowEditing.produto);
            $($(eleRow).find('td')[3]).html(oportunidade.rowEditing.situacao);
            $($(eleRow).find('td')[4]).html(oportunidade.rowEditing.valor);
            $($(eleRow).find('td')[5]).html(oportunidade.rowEditing.ponderado);
            $($(eleRow).find('td')[7]).html(oportunidade.rowEditing.tipotemperatura);
            $($(eleRow).find('td')[10]).html(oportunidade.rowEditing.dtFechamento);

            oportunidade.rowEditing = {};

            $(eleRow).removeClass('editing');
        }
    },

    /**
     * Evento para click do checkbox no filtro de multseleção
     *
     * @return void
     */
    onClickCheckMultSelect: function(event){
        event.preventDefault();
        if($(this).hasClass('icon-checked')){
            $(this).removeClass('icon-checked');
            $(this).addClass('icon-unchecked');
        }else{
            $(this).addClass('icon-checked');
            $(this).removeClass('icon-unchecked');
        }
        return false;
    },

    /**
     * Evento para click do checkbox de MW
     *
     * @return voic
     */
    onClickCheckMW: function(event){
        if($(this).parent().hasClass('mustwinline-table')){
            $(this).parent().parent().find('td').removeClass('mustwinline-table');
        }else{
            $(this).parent().parent().find('td').addClass('mustwinline-table');
        }

        var eleRow = $(this).parent().parent();
        oportunidade.sendCheck($(this).attr('alt'),{'mw' : ($(this).is(':checked'))? 1 : 0},eleRow);
    },

    /**
     * Evento para click do checkbox de BC
     *
     * @return voic
     */
    onClickCheckBC: function(event){
        var eleRow = $(this).parent().parent();
        oportunidade.sendCheck($(this).attr('alt'),{'bc' : ($(this).is(':checked'))? 1 : 0}, eleRow);
    },

    sendCheck: function(id,data, eleRow){
        data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: '/oportunidade/lista/ckeck/'+id+'/',
            type: 'post',
            data: data,
            success: function(response){
                $($(eleRow).find('td')[3]).html(response.situacao);
                console.log('marcação gravada com sucesso');
            },
            error: function(response){
                console.log(response.responseText);
            }
        });
    }
    

}

$(document).ready(function(){
    oportunidade.onReady();
});