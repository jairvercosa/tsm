/**
 * Controller para uso do angularjs na área de equipes
 *
 * @author Jair Verçosa
 * @date 26/03/2014
 */

/*
 * @var object dragStaff - Drag dos elementos do staff
 */
var dragStaff = {
    opacity: 0.7,
    cursorAt: { top: 25, left: 100 },
    containment: $('.row-members-staff'),
    cursor: 'move',
    scroll: true,
    helper: 'clone',
    start: function(e,ui){            
        $(this).draggable( "option", { revert: 'invalid' });
        $('.boxLevels').css('z-index','1');
        $(this).hide();
    },
    stop: function( e, ui ) {
        $(this).css('z-index','0');
        $(this).show();
    }
}

/*
 * @var object dropLevel - Drop dos elementos de staff em níveis
 */
var dropLevel = {
    hoverClass: "ui-state-active",
    drop: function(e, ui){
        var user_id = parseInt($(ui.draggable).find('input[type=hidden]').val());
        var lider_id = null;

        if(typeof $(e.target).find('input[name=membro_id]').val() != 'undefined')
            if($(e.target).find('input[name=membro_id]').val() != '')
                lider_id = parseInt($(e.target).find('input[name=membro_id]').val());

        if(angular.element('.row-members-staff').scope().addMember(user_id, lider_id)){
            $(ui.draggable).remove();
        }
        $('body').css('cursor','auto');
    }
}

//Aplicação front-end equipe
var groupApp = angular.module('groupApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('ngGroupFormCtrl', function ngGroupFormCtrl($scope, $http){
    
    /*
     * @var modelFormContent
     */
     $scope.formContent = "<div></div>";

    /*
     * @var object membroModal - Indica qual o membro está sendo chamado no modal
     */
    $scope.membroModal = {};

    /*
     * @var array staffs - Array com funcionários cadastrados no sistema
     */
    $scope.staffs = [];
    $http.get('/equipe/getstaff/').success(function(data){
        $scope.staffs = data; // response data 
    });

    /*
     * @var array membros - Array com os níveis cadastrados
     */
    $scope.membros = [];

    $scope.loadMembers = function(){
        $scope.membros = [];
        $.ajax({
            async: true,
            type: 'get',
            url : '/equipe/getmembros/',
            success: function(data){
                var items = [], idChield = [], idNext = [];
                var idxToRemove = -1, nivel = 0;

                //Pesquisa o root
                $.each(data,function(i,obj){
                    var match = false;
                    for (var z = data.length - 1; z >= 0; z--) {
                        if(data[z].membro_id == obj.lider_id){
                            match = true;
                            break;
                        }
                    };

                    if(!match){
                        idChield.push(obj.membro_id);
                        data[i].lider_id = null;
                    }
                });

                //Busca os filhos
                while(data.length > 0){
                    items.push([]);
                    idNext = idChield;
                    idChield = [];

                    if(idNext.length==0){
                        break;
                    }

                    //Busca todos os filhos
                    for (var x = idNext.length - 1; x >= 0; x--) {
                        $.each(data,function(i,obj){
                            if(obj.lider_id == idNext[x]){
                                idChield.push(obj.membro_id);
                            }else if(obj.membro_id == idNext[x]){
                                idxToRemove = i;
                                items[nivel].push(obj);
                            }
                        });

                        if(idxToRemove >= 0){
                            data.splice(idxToRemove,1);
                            idxToRemove = -1;
                        }
                    };
                    nivel++;
                }

                $scope.membros = items;
                $scope.makeTree(items);
                $.each($('#chart-container div.node').find('input[name=membro_id]'),function(i,obj){
                    $scope.validGoal($(obj).val());
                });
            },
            error: function(response){ console.log(response.responseText); }
        });
    };
    $scope.loadMembers();

    /*
     * Encontra um membro e retorna um array com a posição de x e y
     */
    $scope.findMember = function(membro_id){
        var x = -1;
        var y = -1;
        $.each($scope.membros,function(i,obj){
            $.each(obj,function(z,item){
                if(item.membro_id == membro_id){
                    x = i;
                    y = z;
                    return false;
                }
            });
        });
        return [x,y]
    };

    /*
     * Encontra um staff e retorna sua posição
     */
    $scope.findStaff = function(user_id){
        var x = -1;
        $.each($scope.staffs,function(i,obj){
            if(obj.user_id == user_id){
                x = i;
                return false;
            }
        });
        return x
    };

    /*
     * Prepara objeto zerando dados manipuláveis
     */
    $scope.prepareItem = function(obj){
        obj.metas = [];
        return obj
    };

    /*
     * Função para executar plugin da hierarquia
     */
    $scope.makeTree = function(items){
        $('#chart-source').html(
            '<li id="id_node_null"> \
                <h5>Organização</h5> \
                <input type="hidden" name="membro_id" value="" /> \
                <ul id="child_node_null"></ul> \
            </li>'
        );
        //$('#chart-source').html('');
        $.each(items,function(i,obj){
            for (var x = obj.length - 1; x >= 0; x--) {
                var eleId = '#chart-source';
                eleId += ' #child_node_'+obj[x].lider_id+'  ';

                $(eleId).append(
                    '<li id="id_node_'+obj[x].membro_id+'"> \
                        <h5>'+obj[x].first_name+' '+obj[x].last_name+'</h5> \
                        <input type="hidden" name="membro_id" value="'+obj[x].membro_id+'" /> \
                        <ul id="child_node_'+obj[x].membro_id+'"></ul> \
                    </li>'
                );
            };
        });
        $('#chart-source').orgChart({container: $('#chart-container')});
        $('#chart-container div.node').droppable(dropLevel);
        $('#chart-container div.node').bind('click',function(){
            var membro_id = $(this).find('input[name=membro_id]').val();
            $scope.onClickMember(membro_id);
        });
        $('.orgChart').css('width', $($('.orgChart table')[0]).width()+120);
        $('.panel-membros-equipe').find('.panel-body').scrollLeft($('.level0-node0').position().left-96)
    };

    /*
     * Adiciona um membro a um líder
     */
    $scope.addMember = function(user_id, lider_id){
        var staff = {};
        var idTemp = new Date().getTime();
        var i = -1;
        var result;

        //Busca o staff
        i = $scope.findStaff(user_id);
        if(i>=0){
            staff = $scope.staffs[i];
            $scope.staffs.splice(i,1);
        }

        staff = $scope.prepareItem(staff);
        staff.lider_id = lider_id;
        staff.membro_id = idTemp;

        if(lider_id==null){
            if($scope.membros.length == 0)
                $scope.membros.push([]);

            $scope.membros[0].push(staff);
        }else{
            //Inclui no nível
            result = $scope.findMember(lider_id);
            if(result[0] >= 0){
                if($scope.membros.length <= (result[0]+1)){
                    $scope.membros.push([]);    
                }
                $scope.membros[result[0]+1].push(staff);
            }
        }
        
        $scope.$apply();
        $scope.makeTree($scope.membros);
        $scope.saveMember(user_id, lider_id, true, idTemp);
        
        return true;
    };

    /*
     * Envia membro para o servidor
     */
    $scope.saveMember = function(user_id, lider_id, async, id_sync){
        var ret = 0;
        var result;

        if(typeof async == 'undefined') async = true;

        $.ajax({
            async: async,
            type: 'POST',
            url : '/equipe/addmembro/',
            data: {
                'csrfmiddlewaretoken'    : $('.row-members-staff input[name="csrfmiddlewaretoken"]').val(),
                'lider_id'                : lider_id,
                'usuario_id'            : user_id
            },
            success: function(response){
                if(response.success){
                    if (typeof id_sync != 'undefined'){
                        result = $scope.findMember(id_sync); //Busca o membro adicionado
                        if(result[0] >= 0){
                            $scope.membros[result[0]][result[1]].membro_id = response.membro_id; //Atualiza com o id retornado
                            if($scope.membros.length > result[0]+1){ //Verifica se existem filhos
                                for (var i = $scope.membros[result[0]+1].length - 1; i >= 0; i--) { //Encontra os filhos
                                    if($scope.membros[result[0]+1][i].lider_id == id_sync){
                                        $scope.membros[result[0]+1][i].lider_id = response.membro_id; //Atualiza o id do lider para os filhos
                                    }
                                };    
                            }
                            //Atualiza o id nos elementos da árvore
                            $('#id_node_'+id_sync).attr('id','id_node_'+response.membro_id);
                            $('#child_node_'+id_sync).attr('id','child_node_'+response.membro_id);
                            $scope.makeTree($scope.membros);
                        }
                    }else{
                        ret = response.membro_id;
                    }

                    $.each($('#chart-container div.node').find('input[name=membro_id]'),function(i,obj){
                        $scope.validGoal($(obj).val());
                    });
                }
                console.log('Membro adicionado');
            },
            error: function(response){ console.log(response.responseText); }
        });

        return ret;
    };

    /*
     * Evento de click do botão remover membro
     */
    $scope.onClickDelMember = function(membro_id){
        var items = [], idChield = [], idNext = [];
        var idxMatch = [];
        var result;
        
        if(!confirm('Atenção, ao remover este membro também serão excluídas as metas atribuídas a ele \
             e todos os membros que ele liderar, bem como suas respectivas metas. Deseja realmente excluir este membro?')){
            return false;
        }

        //Encontra o membro para exclusão
        result = $scope.findMember(membro_id);
        if(result[0] >= 0){
            items.push($scope.membros[result[0]][result[1]]);
            idChield.push($scope.membros[result[0]][result[1]].membro_id);
            item = $scope.prepareItem($scope.membros[result[0]][result[1]]);
            $scope.staffs.push(item);
            idxMatch = [result];    
        }

        //For para cada nível da hierarquia continuando de onde o for anterior parou
        if((idxMatch[0][0]+1) < $scope.membros.length){
            for (var i = idxMatch[0][0]+1; i < $scope.membros.length; i++) {
                idNext = idChield;
                idChield = [];
                //For para cada membro do nível
                $.each($scope.membros[i],function(x,item){
                    //For para pesquisar membros que devem ser removidos
                    for (var y = idNext.length - 1; y >= 0; y--) {
                        if(item.lider_id == idNext[y]){
                            items.push(item);
                            idChield.push(item.membro_id);
                            item = $scope.prepareItem(item);
                            $scope.staffs.push(item);
                            idxMatch.push([i,x]);
                        }
                    };
                });
            };
        }
        $.each(idxMatch,function(i,obj){
            $scope.membros[idxMatch[i][0]].splice(idxMatch[i][1],1);
        });
        
        $('#mdlForm').modal('hide');
        $scope.makeTree($scope.membros);
        //For para excluir dos nós filhos até os nós pais
        for (var i = items.length - 1; i >= 0; i--) {
            $scope.delMember(items[i]);
        };
    };

    /*
     * Remove um membro de um nível
     */
    $scope.delMember = function(member){
        var staff = {};

        $.ajax({
            type: 'post',
            url : '/equipe/delmembro/'+member.membro_id+'/',
            data: {'csrfmiddlewaretoken': $('.row-members-staff').find('input[name=csrfmiddlewaretoken]').val()},
            success: function(response){
                $.each($('#chart-container div.node').find('input[name=membro_id]'),function(i,obj){
                    $scope.validGoal($(obj).val());
                });
                console.log('Membro Removido');
            },
            error: function(response){ console.log(response.responseText); }
        });
        return true;
    };

    /*
     * Evento click do membro
     */
    $scope.onClickMember = function(membro_id){
        var result;

        //Encontra o membro
        result = $scope.findMember(membro_id);
        if(result[0]>=0){
            $scope.membroModal = $scope.membros[result[0]][result[1]];
        }
        
        //Busca formulário para edição
        $.get("/equipe/membro/"+membro_id+"/", function(response){
            $scope.formContent = response;
            $scope.$apply();
            
            //Busca as metas do membro
            $scope.onChangeUserGoal(membro_id);
            $('#id-div-meta-form').html('');
            $.get('/equipe/membro/metas/formulario',function(response){
                $('#id-div-meta-form').html(response);
                $scope.formContent = $('#mdlForm .modal-content').html();
                $scope.$apply();
                
                $('#mdlForm').modal();
                $('#btnRemoveMember').show();
                $('.modal-content small').show();
                $('.frmMembroEdit').on('change',$scope.onChangeFormMember);
                $('.frmMetaEdit ').show();
            })
            
            
        });
    };

    /*
     * Evento para mudança de membro no combo que fica dentro do modal
     */
    $scope.onChangeUserGoal = function(membro_id){
        $scope.$apply();
        
        if($scope.membroModal.metas.length==0){
            $.ajax({
                type : 'GET',
                url  : '/equipe/membro/metas/'+membro_id+'/',
                success : function(response){
                    //Atualiza model principal
                    var result = $scope.findMember(membro_id);
                    $scope.membros[result[0]][result[1]].metas = response; 
                    $scope.membroModal.metas = response;
                    $scope.$apply();
                },
                error : function(response){ console.log('Falha na recuperação das metas'); }
            });
        }
    };

    /*
     * Evento do click do botão adicionar meta do grupo
     */
    $scope.onClickAddGoalGroup = function(){
        var match = false;

        if($('#id_tipometa').val() == "" || $('#id_valor').val() == "" || $('#id_mesVigencia').val() == "" || $('#id_anoVigencia').val() == ""){
            alert('Por favor, preencha todos os campos do formulário.');
            return false;
        };

        if(parseInt($('#id_anoVigencia').val()) < 2000){
            alert('Digite um ano válido.');
            return false;
        };

        //Verifica se este tipo de meta já foi incluído para essa vigência
        $.each($scope.membroModal.metas, function(i,obj){
            if(obj.tipometa == $('#id_tipometa :selected').html()){
                if(obj.mesVigencia == $('#id_mesVigencia').val() 
                    && obj.anoVigencia == parseInt($('#id_anoVigencia').val())
                    && obj.receita == $('#id_receita :selected').html()
                  ){
                    match = true;
                    return false;
                }
            }
        });

        if(match){
            alert('Tipo de Meta já incluída para essa vigência.');
            return false;
        }

        var data = {
            'csrfmiddlewaretoken'   : $('.frmMetaEdit input[name=csrfmiddlewaretoken]').val(), //ponto de atenção
            'criador'               : parseInt($('#id_criador').val()),
            'membro'                : $scope.membroModal.membro_id,
            'receita'               : parseInt($('#id_receita').val()),
            'tipometa'              : parseInt($('#id_tipometa').val()),
            'valor'                 : parseFloat($('#id_valor').val()),
            'mesVigencia'           : $('#id_mesVigencia').val(),
            'anoVigencia'           : parseInt($('#id_anoVigencia').val())
        };
        var idx = 0;
        $scope.membroModal.metas.push({
            id          : 0,
            tipometa    : $('#id_tipometa :selected').html(),
            receita     : $('#id_receita :selected').html(),
            valor       : data.valor,
            mesVigencia : data.mesVigencia,
            anoVigencia : data.anoVigencia
        });
        idx = $scope.membroModal.metas.length - 1;
        $('#id_tipometa').val('');
        $('#id_valor').val('');
        $('#id_tipometa').focus();

        $.ajax({
            type: 'post',
            url: '/equipe/membro/metas/formulario/',
            data: data,
            success: function(response){
                var result = $scope.findMember($scope.membroModal.membro_id);
                $scope.validGoal($scope.membroModal.lider_id);
                $scope.validGoal($scope.membroModal.membro_id);
                $scope.membroModal.metas[idx].id = response.id;
                $scope.membros[result[0]][result[1]].metas = $scope.membroModal.metas;
            },
            error: function(response){
                $scope.membroModal.metas.splice(idx,1);
                if(typeof response.message == 'undefined'){
                    console.log(response.responseText);
                    alert('Desculpe, mas a meta não pode ser incluída');
                }else{ alert(response.message); }
            }
        });
    };

    /*
     * Evento do click do botão remover meta do grupo
     */
    $scope.onClickDelGoalGroup = function(goal_id){
        if($scope.membroModal.membro_id == idMemberUser) return false;
        if(!confirm('Deseja realmente remover esta meta?')) return false;

        $.each($scope.membroModal.metas,function(i,obj){
            if(obj.id == goal_id){
                $.ajax({
                    type: 'post',
                    url: '/equipe/membro/metas/remove/'+goal_id+'/',
                    data : {'csrfmiddlewaretoken':$('.frmMetaEdit input[name=csrfmiddlewaretoken]').val()},
                    success: function(response){
                        var result = $scope.findMember($scope.membroModal.membro_id);
                        $scope.validGoal($scope.membroModal.lider_id);
                        $scope.validGoal($scope.membroModal.membro_id);
                        $scope.membroModal.metas.splice(i,1);
                        $scope.membros[result[0]][result[1]].metas = $scope.membroModal.metas;
                        $scope.$apply();
                    },
                    error: function(response){ console.log(response.responseText); }
                });
                return false;
            }
        });
    };

    /*
     * Evento de click para o checkbox de visibilidade da meta pelo membro do grupo
     */
    $scope.onClickCheckGoal = function(goal_id){
        if($scope.membroModal.membro_id == idMemberUser) return false;

        $.each($scope.membroModal.metas,function(i,obj){
            if(obj.id == goal_id){
                $scope.membroModal.metas[i].isVisible = !obj.isVisible;

                $.ajax({
                    type : 'POST',
                    url  : '/equipe/membro/metas/visivel/'+goal_id+'/',
                    data : {
                        'csrfmiddlewaretoken':$('.frmMetaEdit input[name=csrfmiddlewaretoken]').val(),
                        'isVisible' : $scope.membroModal.metas[i].isVisible
                    },
                    success : function(response){
                        var result = $scope.findMember($scope.membroModal.membro_id);
                        console.log('Visibilidade Alterada');
                        $scope.membros[result[0]][result[1]].metas = $scope.membroModal.metas;
                        $scope.validGoal($scope.membros[result[0]][result[1]].membro_id);
                    },
                    error : function(response){ console.log('Falha na atualização da visibilidade'); }
                });

                return false;
            }
        });
    };

    /*
     * Valida se um membro tem todas as metas atribuídas aos seus liderados
     */
    $scope.validGoal = function(membro_id){
        if(membro_id==null || membro_id == '') return false;
        
        $.ajax({
            type : 'GET',
            url  : '/equipe/membro/metas/valida/'+membro_id+'/',
            success : function(response){
                var ele = $('input[value="'+membro_id+'"]').parent('h2').parent('div');
                if(!response.result){
                    $(ele).attr('data-toggle','popover');
                    $(ele).attr('data-content',response.message);
                    $(ele).attr('data-original-title','Atenção');
                    $(ele).addClass('with-error');
                    $(ele).popover({ trigger: 'hover', html : true });
                }else{
                    $(ele).removeClass('with-error');
                    $(ele).popover('destroy');
                }
            },
            error : function(response){ console.log('Falha na validação da meta'); }
        });
        return true;
    }

    /* Evento para mudanças realizadas no formulário de membro
     *
     * @return void
     */
    $scope.onChangeFormMember = function(event){
        var unindexed_array = $(this).serializeArray();
        var indexed_array = {};
        
        $.map(unindexed_array, function(i, item){
            if(!$(item).hasClass('custom-combobox-input')){ //Ignora campos vindos da customização de combo autocomplete
                //Tratamento para campos multseleção
                if ($('[name='+i['name']+'] :selected').length > 0 && typeof $('[name='+i['name']+']').attr('multiple') != 'undefined'){
                    if(typeof indexed_array[i['name']+'[]'] == 'undefined')
                        indexed_array[i['name']+'[]'] = [];

                    indexed_array[i['name']+'[]'].push(i['value']);
                }else{
                    indexed_array[i['name']] = i['value'];
                }
            }
        });

        $.ajax({
            type : 'POST',
            url  : '/equipe/membro/'+$scope.membroModal.membro_id+'/',
            data : indexed_array,
            success: function(data){
                $scope.loadMembers();
            },
            error : function(response){ 
                console.log('Falha na gravação do formulário de membros'); 
                console.log(response);
            }
        });

    };
});

/*
 * Directive para drag do staff
 */
groupApp.directive("myStaff", [
    '$document',
    function($document) {
        return function(scope,element,attr){
            $(element).draggable(dragStaff);
            $(element).fadeIn('fast');
        }
    }
]);

/*
 * Directive para html dinamico do modal
 */
groupApp.directive("dynamic", function($compile){
    return {
        restrict: 'A',
        replace: true,
        link: function (scope, ele, attrs){
            scope.$watch(attrs.dynamic, function(formContent){
                ele.html(formContent);
                $compile(ele.contents())(scope);
            });
        }
    };
});

/*
 * Directive para metas
 */
groupApp.directive("visibleOnAdd",[
    '$document',
    function($document){
        return function(scope, element, attr){
            $(element).fadeIn('fast');
        }
    }
]);