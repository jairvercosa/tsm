/**
 * Controller para uso do angularjs no formulário de oportunidades
 *
 * @author Jair Verçosa
 * @date 27/04/2014
 */

//Aplicação front-end
var opApp = angular.module('opApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('ngOpFormCtrl', function ngOpFormCtrl($scope, $http){

    /*
     * Valor atual da combo de responsável
     */
    $scope.responsavel_id = $('#id_responsavel').val();

    /*
     * Evento de click do botão de status da questão
     */
    $scope.onClickBtnStatusQuestao = function(e){
        var resposta = $(this).parent().find('input[name=valResposta]').val() == 'True' ? true : false;

        if(resposta){
            $(this).parent().find('input[name=valResposta]').val('False');
            $(this).html('Não');
        }else{
            $(this).parent().find('input[name=valResposta]').val('True');
            $(this).html('Sim');
        }

        if($(this).hasClass('btn-success')){
            $(this).removeClass('btn-success');    
            $(this).addClass('btn-danger');
        }else{
            $(this).removeClass('btn-danger');
            $(this).addClass('btn-success');
        }

        $scope.calculaTemp();
        return true;
    };

    /**
     * Calcula temperatura automática
     */
    $scope.calculaTemp = function(){
        var dataPost = []

        $.each($('.ul-perguntas li'),function(i,obj){
            var id = $(obj).find('input[name=idQuestao]').val();
            var resposta = $(obj).find('input[name=valResposta]').val();

            dataPost.push('{"id": '+id+',"resposta": '+resposta+'}');
        });

        $.ajax({
            type: 'post',
            url: '/oportunidade/calculatemp/',
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'respostas':dataPost
            },
            success: function(response){
                if(response.success){
                    $('#id_temperatura_auto').val(response.temperatura);
                }
            },
            error: function(response){
                console.log('Falha no cálculo da temperatura');
                console.log(response.responseText);
            }
        });
        
        return true;
    };

    /*
     * Evento para mudança de responsável
     */
    $scope.onChangeResponsavel = function(e){
        var id = $(this).val()

        if($(this).val()=='' || $scope.responsavel_id == id){
            return false;
        }

        $scope.responsavel_id = id;
        $('#id_lider').hide();
        $('#id_lider').parent().append('<span class="loadingData"><img src="/static/img/ajax-loader.gif" /></span>');
        $http.get('/oportunidade/formulario/getlider/'+id+'/').success(function(data){
            $('#id_lider').html('<option value selected="selected">---------</option>');
            $.each(data,function(i,obj){
                $('#id_lider').append('<option value="'+obj.id+'">'+obj.first_name+' '+obj.last_name+'</option>');
            });
            $('.loadingData').remove();
            $('#id_lider').show();
        });
    };

    /*
     * Atribui bind dos elementos html
     */
    $('.ul-perguntas li div button').bind('click',$scope.onClickBtnStatusQuestao);
    $('#id_responsavel').on('change',$scope.onChangeResponsavel);

    /*
     * Atribui datepicker 
     */
    $('#id_dtFechamento').datepicker(app.datePickerBr);

    /*
     * Sobrescreve método salvar para enviar as repostas também
     */
    form.fnGetDataAsJson = function(){
        var unindexed_array = $(form.formObject).serializeArray();
        var indexed_array = {};
        var respostas = [];
        
        $.map(unindexed_array, function(i, item){
            //Tratamento para campos multseleção
            if ($('[name='+i['name']+'] :selected').length > 0 && typeof $('[name='+i['name']+']').attr('multiple') != 'undefined'){
                if(typeof indexed_array[i['name']+'[]'] == 'undefined')
                    indexed_array[i['name']+'[]'] = [];

                indexed_array[i['name']+'[]'].push(i['value']);
            }else{
                indexed_array[i['name']] = i['value'];
            }
        });

        //Envia respostas também
        $.each($('input[name=valResposta]'),function(i,obj){
            var id = $(obj).parent().find('input[name=idQuestao]').val()
            respostas.push('{"questao":'+id+', "resposta": '+$(obj).val()+'}');
        });

        indexed_array['respostas'] = respostas;

        //Atribui campos que podem estar desabilitados
        $.each($('input[disabled="True"]'),function(i,obj){
            var field_name = $(obj).attr('id').substr(3);
            indexed_array[field_name] = $(obj).val();
        });

        $.each($('select[disabled="True"]'),function(i,obj){
            var field_name = $(obj).attr('id').substr(3);
            indexed_array[field_name] = $(obj).val();
        });

        $.each($('textarea[disabled="True"]'),function(i,obj){
            var field_name = $(obj).attr('id').substr(3);
            indexed_array[field_name] = $(obj).val();
        });
        
        return indexed_array;
    }

    if(!$('#id_cliente').is(':disabled')){
        //Atribui click ao botão de adicionar novo no campo de cliente
        $('#id_cliente').parent().find('.btn-add-combo').bind('click',function(){
            app.addModal('/cliente/clientes/formulario/min/',function(){
                formAjax.fnAfterPost = function(result){
                    $('#id_cliente').append('<option value="'+result.pk+'">'+$('#formClientes').find('#id_nome').val()+'</option>');
                    $('.modalFromAjax').modal('hide');
                    $('#id_cliente option').eq($('#id_cliente option').length-1).prop('selected', true);
                    $('#id_cliente').parent().find('.custom-combobox-input').val($('#formClientes').find('#id_nome').val());    
                    $('#id_cliente').combobox();
                }
            });
        });

        $('#id_cliente').combobox();
    }

    //Sobreescrve método de redirection do form
    form.fnRedirectAfterPost = function(){
        window.location.href = form.urlRedirection;
    };

    //Atribui clicks do rtc
    $('#btnRtcCompleto').bind('click',function(){
        window.location.href = 'rtc';
    });

    $('#btnAddRtc').bind('click',function(){
        var fnRedirectAfterPost = form.fnRedirectAfterPost;
        form.fnRedirectAfterPost = function(result){
            var href = '';
            if(typeof result.pk != 'undefined')
                href = '/oportunidade/lista/'+result.pk+'/rtc/formulario?return';
            else
                href = 'rtc/formulario?return';
            
            window.location.href = href;
        }
        form.fnOnError = function(){
            form.fnRedirectAfterPost = fnRedirectAfterPost;
        }

        form.fnSubmitForm();
    });
});