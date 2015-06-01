/**
 * Controller para uso do angularjs no dashboard
 *
 * @author Jair Verçosa
 * @date 30/04/2014
 */


//Aplicação front-end dashboard
var viewDashboardApp = angular.module('viewDashboardApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).controller('ngViewDashboardCtrl', function ngViewDashboardCtrl($scope, $http){
    /**
     * @var rgraph errorParamsMessage
     */
    $scope.errorParamsMessage = [{
        message: 'Excelente trabalho. Você faz a diferença neste time!!',
        class: 'alert-success'
    },{
        message: 'Você está indo bem! Seus indicadores mostram que você está no caminho certo, mas pode melhorar. Analise as mensagens abaixo \
        para que você faça sua meta de maneira mais sustentável.',
        class: 'alert-info'
    },{
        message: 'Tenha mais atenção a esses números! Ajustes seus indicadores rapidamente para que consiga fazer sua meta até o final do período.',
        class: 'alert-yellow'
    },{
        message: 'Repense sua estratégia! Você está em uma zona de risco e perigosa, pode ser que não alcance suas metas. Veja as mensagens abaixo dos indicadores \
        e melhore rápidamente seus números para virar esse jogo.',
        class: 'alert-warning'
    },{
        message: 'Atenção! Seus números não estão adequados, ajuste urgentemente seu forecast. Neste caminho você não alcançará sua meta!',
        class: 'alert-danger'
    }];

    /**
     * @var rgraph errorParams
     */
    $scope.errorParams = 0;

    /**
     * @var rgraph chart_ponderado
     */
    $scope.chart_ponderado = null;

    /**
     * @var array of rgraph chart_evolucaopl
     */
    $scope.chart_evolucaopl = [];

    /**
     * @var rgraph chart_gross
     */
    $scope.chart_gross = null;

    /**
     * @var rgraph chart_gross_meta
     */
    $scope.chart_gross_meta = null;

    /**
     * @var rgraph chart_compromisso
     */
    $scope.chart_compromisso = [];

    /**
     * @var rgraph chart_linearidade
     */
    $scope.chart_linearidade = [];    

    /**
     * @var obj linearidadeData
     */
    $scope.linearidadeData = [];

    /**
     * @var obj linearidadeHead
     */
    $scope.linearidadeHead = [];

    /**
     * @var obj linearidadeFoot
     */
    $scope.linearidadeFoot = [];

    /**
     * @var obj objFiltro
     */
    $scope.objFiltro = {
        tipometa: '',
        membro: '',
        diaIni: '',
        diaFim: '',
        receitas: ''
    }

    /**
     * Carrega os dados via ajax para os gráficos
     *
     * @return obj
     */
    $scope.loadData = function(callBack){
        var dictReturn = {};
        var receitas = [];
        $scope.objFiltro.diaIni = $('#id_dia_ini').val();
        $scope.objFiltro.diaFim = $('#id_dia_fim').val();
        //$scope.closeFormDate();

        $scope.toggleLoading();

        tipovisao = $('#id_visao').val().substr(0,6) == 'filial' ? 'filial' : 'usuario';
        visao = $('#id_visao').val().substr(0,6) == 'filial' ? $('#id_visao').val().substr(7) : $('#id_visao').val().substr(8);

        var receitasStr = '';
        $.each($('.div-dashboard-receitas ul li a.icon-checked'),function(i,obj){
            receitas.push($(obj).attr('alt'));
            receitasStr += $(obj).html();
            if(i==$('.div-dashboard-receitas ul li a.icon-checked').length-2){
                receitasStr += ' e '
            }else{
                receitasStr += ', '
            }
        });

        $scope.objFiltro.membro = $('#id_visao option:selected').html();
        $scope.objFiltro.tipometa = $('#id_tipo_meta option:selected').html();
        $scope.objFiltro.receitas = receitasStr.substr(0,receitasStr.length-2);

        data = {
            "visao" : visao,
            "tipovisao": tipovisao,
            "tipometa": $('#id_tipo_meta').val(),
            "diaini": $('#id_dia_ini').val(),
            "diafim": $('#id_dia_fim').val(),
            "receitas": receitas
        }

        $.ajax({
            type: 'GET',
            url : '/oportunidade/dashboard/data/',
            data: data,
            success: function(response){
                dictReturn = response;

                if(typeof callBack == 'function')
                    callBack(dictReturn);
            },
            error: function(response){ console.log(response.responseText); }
        });

        return dictReturn;
    }

    /**
     * Atualiza gráficos
     *
     * @return boolean
     */
    $scope.refreshCharts = function(){
        $('canvas').hide();
        $scope.loadData(function(data){
            if(data == null){
                return false;
            }

            $('.messageDash').fadeOut();
            $('p.aviso').html('');
            $scope.errorParams = 0;

            $('canvas').fadeIn('fast');
            $scope.toggleLoading();
            $scope.makeChartPonderado(data.ponderado);
            //$scope.makeChartEvolucaoPl(data.evolucao);
            $scope.makeChartGross(data.gross);
            $scope.makeChartLinearidade(data.linearidade);
            $scope.makeChartCompromisso(data.compromisso);

            $('.messageDash').removeClass('alert-danger');
            $('.messageDash').removeClass('alert-warning');
            $('.messageDash').removeClass('alert-yellow');
            $('.messageDash').removeClass('alert-info');
            $('.messageDash').removeClass('alert-success');

            //$scope.objFiltro
            /*if($scope.errorParams<=($scope.errorParamsMessage.length-1)){
                $('.page-header .alert p.aviso').html($scope.errorParamsMessage[$scope.errorParams].message);
                $('.messageDash').addClass($scope.errorParamsMessage[$scope.errorParams].class);
            }else{
                $('.page-header .alert p.aviso').html($scope.errorParamsMessage[$scope.errorParamsMessage.length-1].message);
                $('.messageDash').addClass($scope.errorParamsMessage[$scope.errorParamsMessage.length-1].class);
            }
            $('.page-header .alert').fadeIn();*/
        });

        return true;
    }

    /**
     * Cria o gráfico ponderado
     *
     * @return void
     */
    $scope.makeChartPonderado = function(data){
        if($scope.chart_ponderado != null){
            RGraph.ObjectRegistry.Remove($scope.chart_ponderado);
        }

        var tooltips = []
        var totalizer = {
            ponderado: 0,
            desencaixe: 0,
            compensacao: 0
        }
        $.each(data.values,function(i,obj){
            tooltips.push('R$ '+$.number(obj,2));
        });

        $scope.chart_ponderado = new RGraph.Bar('id_chart_ponderado', data.data)
                                        .set('title', 'Meta x Ponderado')
                                        .set('colors', ["#0c72b0", "#86dc6f", "#EAA228"])
                                        .set('labels', data.labels)
                                        .set('gutter.top', 40)
                                        .set('gutter.left', 40)
                                        .set('gutter.bottom', 50)
                                        .set('key.position.y', 310)
                                        .set('text.size',10)
                                        .set('hmargin', 5)
                                        .set('labels.above', false)
                                        .set('units.post', '%')
                                        .set('key.position', 'gutter')
                                        .set('key.position.gutter.boxed', false)
                                        .set('key', ['2x Meta','Meta','Ponderado'])
                                        .set('noxaxis', true)
                                        .set('xlabels', false)
                                        .set('tooltips', tooltips)
                                        .set('shadow', true)
                                        .set('shadow.blur',2)
                                        .grow();

        $('#id_ponderado_desencaixe tbody').html('');
        $.each(data.table_data,function(i,obj){
            $('#id_ponderado_desencaixe tbody').append(
                '\
                <tr>\
                    <th>'+obj.title+'</th>\
                    <th class="text-red hidden-xs"><span>R$</span> '+$.number(obj.ponderado,2)+'</th>\
                    <th class="text-red"><span class="hidden-xs">R$</span> '+$.number(obj.desencaixe,2)+'</th>\
                    <th class="text-red hidden-xs"><span>R$</span> '+$.number(obj.compensacao,2)+'</th>\
                    <th>'+$.number(obj.fatorx,2)+'</th>\
                </tr>\
                '
            );

            totalizer.ponderado += obj.ponderado;
            totalizer.desencaixe += obj.desencaixe;
            totalizer.compensacao += obj.compensacao;

        });

        $('#id_ponderado_desencaixe tfoot').html(
            '\
            <tr class="hidden-xs">\
                <th></th>\
                <th>'+$.number(totalizer.ponderado,2)+'</th>\
                <th>'+$.number(totalizer.desencaixe,2)+'</th>\
                <th>'+$.number(totalizer.compensacao,2)+'</th>\
                <th></th>\
            </tr>\
            '
        );

        /*if(!data.ok){
            $scope.errorParams++;
            $('.panel-prospeccao').find('.aviso').html('Você precisa prospectar mais, trabalhe sua carteira de clientes e aumente suas oportunidades.');
            $('.panel-prospeccao').find('.messageDash').fadeIn();
        }*/
    }

    /**
     * Cria painel de evolução do pipeline
     *
     * @return void
     */
    $scope.makeChartEvolucaoPl = function(data){
        var tableHeader = '';

        if($scope.chart_evolucaopl.length > 0){
            $.each($scope.chart_evolucaopl,function(i,obj){
                RGraph.ObjectRegistry.Remove($scope.chart_evolucaopl[i]);
            });
        }

        $.each(data.tipos,function(x,item){
            tableHeader += '<th>'+item+'</th>';
        })

        $scope.chart_evolucaopl = [];
        $('.panel-evolucao-pipeline').html('');
        $.each(data.data,function(i,obj){
            var idChart = 'id_chart_evolucao_'+i;
            var tooltips = [];
            var tablePonderado = '';
            
            $.each(obj.grafico,function(x,item){
                tooltips.push('R$ '+$.number(item,2));
            });

            $.each(obj.table_data,function(x,item){
                var classe = '';
                if(item.substr(0,1)=='R')
                    classe = 'text-red';
                else
                    classe = 'text-green';

                item = item.substr(1);

                tablePonderado += '<th class="'+classe+'">'+item+'%</th>';
            });
            tablePonderado += '<th>'+$.number(obj.fatorx,2)+'</th>';          

            $('.panel-evolucao-pipeline').append('\
                <div class="row"> \
                    <div class="col-lg-2"> \
                        <h4>'+obj.nome+'</h4> \
                    </div> \
                    <div class="col-lg-6"> \
                        <table class="table table-striped table-hover"> \
                            <thead> \
                                <tr>'+tableHeader+'</tr> \
                            </thead> \
                            <tbody> \
                                <tr>'+tablePonderado+'</tr> \
                            </tbody> \
                        </table> \
                    </div> \
                    <div class="col-lg-4"> \
                        <canvas id="'+idChart+'" width="220" height="111">[No canvas support]</canvas> \
                    </div> \
                </div> \
            ');
            var chart = new RGraph.HBar(idChart, [obj.grafico])
                                .set('colors', ["#b81b06", "#d08e27"])
                                .set('gutter.left', 0)
                                .set('gutter.right', 90)
                                .set('text.size',10)
                                .set('hmargin', 5)
                                .set('units.pre', 'R$ ')
                                .set('key.position', 'gutter')
                                .set('key.position.gutter.boxed', false)
                                .set('key', ['Meta','Ponderado'])
                                .set('labels.above', true)
                                .set('labels.above.decimals', 2)
                                .set('noxaxis', true)
                                .set('xlabels', false)
                                .set('tooltips', tooltips)
                                .set('shadow', false)
                                .grow()
            $scope.chart_evolucaopl.push(chart);

        });
    }

    /**
     * Cria gráfico do gross
     * 
     * @return vois
     */
    $scope.makeChartGross = function(data){
        var tooltips = [];
        var labels = [];

        if($scope.chart_gross != null ){
            RGraph.ObjectRegistry.Remove($scope.chart_gross);
            //RGraph.ObjectRegistry.Remove($scope.chart_gross_meta);
        }

        $.each(data.values,function(x,item){
            tooltips.push('R$ '+$.number(item,2));
        });

        $.each(data.data,function(x,item){
            labels.push(item+'%');
        });

        $('#id_chart_gross').parent().find('h4').html('Total R$ '+$.number(data.total,2));
        $('#id_chart_gross').parent().find('h5').html('Total Fechado: R$ '+$.number(data.fechado,2));
        $scope.chart_gross = new RGraph.Pie('id_chart_gross', data.data)
                                    .set('title', 'Oportunidades')
                                    .set('title.y',20)
                                    .set('colors', ["#6aac2a", "#f1ea30", "#e0672d"])
                                    .set('labels.ingraph',true)
                                    .set('labels.ingraph.specific',labels)
                                    .set('tooltips', tooltips)
                                    .set('key', data.tipos)
                                    .set('key.position', 'gutter')
                                    .set('key.position.gutter.boxed', false)
                                    .set('key.position.y', 272)
                                    .roundRobin();

        /*if(!data.ok){
            $scope.errorParams++;
            if((data.total-data.fechado)>0)
                $('.panel-gross').find('.aviso').html('Aqueça mais suas oportunidades!');
            else
                $('.panel-gross').find('.aviso').html('Inclua oportunidades, seu pipeline está zerado!');
            $('.panel-gross').find('.messageDash').fadeIn();
        }*/
        /*$scope.chart_gross_meta = new RGraph.Bar('id_chart_gross_meta',data.meta)
                                            .set('title', 'Meta x Oportunidades')
                                            .set('background.myBarcolor1', 'white')
                                            .set('labels', data.tipos)
                                            .set('linewidth', 2)
                                            .set('gutter.top', 40)
                                            .set('gutter.left', 40)
                                            .set('gutter.bottom', 50)
                                            .set('key.position.y', 200)
                                            .set('background.myBarcolor2', 'white')            
                                            .set('noyaxis',true)
                                            .set('noxaxis',true)
                                            .set('hmargin', 10)
                                            .set('units.post', '%')
                                            .set('colors', ["#a6bce8", "#1847a7"])
                                            .set('shadow', true)
                                            .set('shadow.blur',2)
                                            .set('grouping', 'stacked')
                                            .set('key', ['Meta','Oportunidades'])
                                            .set('labels.above',false)
                                            .set('key.position', 'gutter')
                                            .set('key.position.gutter.boxed', false)
                                            .grow();*/
    };

    /**
     * Função criar tabela de linearidade
     *
     * @return void
     */
    $scope.makeChartLinearidade = function(data){
        $scope.linearidadeData = data;
        $scope.linearidadeHead = [];
        $scope.linearidadeFoot = [];

        var dias = [];
        var dados = [[],[]];
        var metaGeral = 0;

        //Monta cabeçalho
        $.each(data[0].items,function(i,obj){
            dias.push(obj.dia.substr(0,2));

            $scope.linearidadeHead.push({
                dia: obj.dia.substr(0,2),
                percentual: obj.indicador+obj.percentmeta+'%'
            });

            $scope.linearidadeFoot.push({
                "meta": 0,
                "valor": 0,
                "percent": 0
            })
        });

        //Monta footer (somatório)
        $.each(data,function(i,obj){
            $.each(obj.items,function(x,linha){
                metaGeral += linha.meta;
                $scope.linearidadeFoot[x].meta += linha.meta;
                $scope.linearidadeFoot[x].valor += linha.ponderado;
                //$scope.linearidadeFoot[x].percent = (($scope.linearidadeFoot[x].valor/$scope.linearidadeFoot[x].meta)*100)
            });
        });

        //Calcula o percentual baseado na meta cheia
        $.each($scope.linearidadeFoot,function(i,obj){
            $scope.linearidadeFoot[i].percent =  $.number(($scope.linearidadeFoot[i].valor/$scope.linearidadeFoot[$scope.linearidadeFoot.length-1].meta)*100,2)
        });

        //Valida percentual
        /*$.each($scope.linearidadeFoot, function(i,obj){
            if(obj.meta>obj.valor){
                $('.panel-linearidade').find('.aviso').html('Você precisa entregar mais no prazo.');
                $('.panel-linearidade').find('.messageDash').fadeIn();
                $scope.errorParams++;
                return false;
            }
        });*/

        //Monta o gráfico de linearidade
        var tooltips = [];
        $.each($scope.linearidadeFoot,function(i,obj){
            dados[0].push(obj.meta);
            dados[1].push(obj.valor);
        });

        $.each(dados,function(i,obj){
            $.each(obj,function(x,item){
                tooltips.push('R$ '+$.number(item,2));
            });
        });


        var title = $('#id_visao option:selected').html();
        if($scope.chart_linearidade.length > 0){
            $.each($scope.chart_linearidade,function(i,obj){
                RGraph.ObjectRegistry.Remove(obj);    
            })
            $scope.chart_linearidade = [];
            $('#div-chart-linearidade').find('canvas').remove();
            $('#div-chart-linearidade').append('<canvas id="id_chart_linearidade" class="chart_linearidade" height="250">[No canvas support]</canvas>')
        }

        var tamLinearidade = $('#div-chart-linearidade').find('.col-lg-12').width();
        $('#div-chart-linearidade').find('canvas').attr('width',tamLinearidade);


        $scope.chart_linearidade.push(new RGraph.Line('id_chart_linearidade', dados[0],dados[1])
                .set('background.grid.autofit.numhlines', 10)
                .set('title', title)
                .set('title.y',20)
                .set('labels', dias)
                .set('units.pre', 'R$ ')
                .set('gutter.left', 100)
                .set('linewidth',2)
                .set('filled', true)
                .set('filled.range', true)
                .set('filled.range.threshold', 10)
                .set('filled.range.threshold.colors', ['#b2ebf2','#ffcc80'])
                .set('fillstyle', 'red')
                .set('colors', ['#e65100', '#00838f'])
                .set('key', ['Meta','Oportunidades'])
                .set('key.position', 'gutter')
                .set('key.position.gutter.boxed', false)
                .set('key.position.x', 900)
                .set('key.position.y', 0)
                .set('tooltips', tooltips)
                .draw());

        $scope.$apply();
    };

    /**
     * Função para gráfico de Meta x Compromisso
     *
     * @return void
     */
    $scope.makeChartCompromisso = function(data){
        if($scope.chart_compromisso.length > 0){
            $.each($scope.chart_compromisso,function(i,obj){
                RGraph.ObjectRegistry.Remove(obj);
            });
        }

        //Monta Gráficos
        var tamChart = null
        var legendSituacao = '';
        $('#id-indicadores-pedra').html('');
        $.each(data.table_data,function(i,obj){
            $('#id-indicadores-pedra').append('<div class="col-lg-2 padding-no-xs"><canvas class="canvas-chart-pedra" id="id_chart_compromisso_'+i+'">[No canvas support]</canvas></div>');
            if(tamChart==null){
                tamChart = $('#id-indicadores-pedra .col-lg-2').width();
            }
        });

        $.each($('.canvas-chart-pedra'),function(x,item){
            $(item).attr('width',tamChart);
            $(item).attr('height',tamChart);

            var total = 0;
            var dataPie = [];
            var situacoes = [];
            var labels = [];
            $.each(data.table_data[x].itemsSituacao,function(y,obj){
                total += obj.valor; //Monta o somatório das oportunidades nas situações
                dataPie.push(obj.valor); //Guarda o valor da situação para calcular o percentual
                situacoes.push(obj.nome); //Nome a situação (pedra/upside)
            });

            $.each(dataPie,function(y,obj){
                dataPie[y] = Math.round((obj/total)*100,2);
                labels.push($.number(dataPie[y])+'%');
            });

            $scope.chart_compromisso.push(new RGraph.Pie($(item).attr('id'), dataPie)
                                    .set('title', data.table_data[x].title)
                                    .set('title.y',20)
                                    .set('colors', ["#86dc6f", "#EAA228", "#52c7e4", "#308dc6"])
                                    .set('labels.ingraph',true)
                                    .set('labels.ingraph.specific',labels)
                                    .set('key', situacoes)
                                    .set('key.position', 'gutter')
                                    .set('key.position.gutter.boxed', false)
                                    .set('key.position.y', tamChart-15)
                                    .roundRobin());

            if(legendSituacao==''){
                $.each(situacoes,function(y,z){
                    legendSituacao += ' x '+z;
                });
            }
        });
        $('#id-legend-situacao').html(legendSituacao.substr(3));

        var tooltips = []
        $.each(data.values,function(i,obj){
            tooltips.push('R$ '+$.number(obj,2));
        });

        //Indicador meta x compromissado
        $('#id-indicadores-pedra').append('<div class="col-lg-6 padding-no-xs"><canvas id="id_chart_compromisso">[No canvas support]</canvas></div>');
        $('#id_chart_compromisso').attr('height',tamChart);

        var positionLegendY = tamChart;
        tamChart = $('#id-indicadores-pedra .col-lg-6').width();
        $('#id_chart_compromisso').attr('width',tamChart);
        

        $scope.chart_compromisso.push(new RGraph.Bar('id_chart_compromisso', data.data)
                                        .set('title', 'Meta x Compromissado')
                                        .set('colors', ["#86dc6f", "#52c7e4", "#EAA228", "#308dc6"])
                                        .set('labels', data.labels)
                                        .set('gutter.top', 40)
                                        .set('gutter.bottom', 40)
                                        .set('gutter.left', 86)
                                        .set('text.size',10)
                                        .set('hmargin', 15)
                                        .set('labels.above', false)
                                        .set('units.pre', 'R$ ')
                                        .set('key.position', 'gutter')
                                        .set('key.position.gutter.boxed', false)
                                        .set('key.position.y', positionLegendY-12)
                                        .set('key.position.x', 10)
                                        .set('key', data.legenda)
                                        .set('noxaxis', true)
                                        .set('xlabels', false)
                                        .set('tooltips', tooltips)
                                        .set('shadow', true)
                                        .set('shadow.blur',2)
                                        .grow());

        //Monta tabela de resumo
        var totalizador = {
            "itemsSituacao": [],
            "realizado": 0,
            "corrigida": 0,
            "medicao": 0,
            "meta": 0,
            "valFatorPond": 0,
            "percent": 0
        }
        var headerSituacao = '';
        var headerMedicao = '';
        if(data.table_data.length > 0){
            //Monta colunas do cabeçalho para situações
            var itemsSituacao = data.table_data[0].itemsSituacao;
            $.each(itemsSituacao,function(x,item){
                headerSituacao += '<th width="7%" class="th-label hidden-xs">\
                                        <a class="no-action" \
                                            data-toggle="tooltip" \
                                            data-placement="top" \
                                            title="" data-original-title="Qtd. de negócios em '+item.nome+'"\
                                        >Neg. em '+item.nome+'</a>\
                                    </th>';
                headerSituacao += '<th class="th-label hidden-xs">\
                                        <a class="no-action" \
                                            data-toggle="tooltip" \
                                            data-placement="top" \
                                            title="" data-original-title="FCST gross em '+item.nome+'"\
                                        >FCST '+item.nome+'</a>\
                                    </th>';
                headerMedicao += '/'+item.nome.substr(0,1);

                //Adiciona linha no totalizador
                totalizador.itemsSituacao.push([0,0])
            });
            headerMedicao = headerMedicao.substr(1);
        }

        var headerTable = '\
            <tr>\
                <th></th>\
                <th class="th-label">\
                    <a class="no-action" \
                        data-toggle="tooltip" \
                        data-placement="top" \
                        title="" data-original-title="Total de oportunidades fechadas"\
                    >Fechado</a>\
                </th>\
                <th class="th-label hidden-xs ">\
                    <a class="no-action" \
                        data-toggle="tooltip" \
                        data-placement="top" \
                        title="" data-original-title="Meta sem oportunidades fechadas"\
                    >Corrigida</a>\
                </th>'+headerSituacao+'\
                <th class="th-label">\
                    <a class="no-action" \
                        data-toggle="tooltip" \
                        data-placement="top" \
                        title="" data-original-title="Valor ponderado das oportunidades."\
                    >'+headerMedicao+'</a>\
                </th>\
                <th class="th-label hidden-xs hidden-sm fator-pond"></th>\
                <th class="th-label ">\
                    <a class="no-action padding-left-10" \
                        data-toggle="tooltip" \
                        data-placement="left" \
                        title="" data-original-title="Percentual atingido da meta com as oportunidades fechadas."\
                    >Att%</a>\
                </th>\
            </tr>\
        ';
        $('#id_compromisso thead').html(headerTable);
        $('#id_compromisso tbody').html('');
        $.each(data.table_data,function(i,obj){
            

            //Cria colunas das situações
            var bodySituacao = '';
            if(obj.itemsSituacao.length > 0){
                //Monta colunas do cabeçalho para situações
                $.each(obj.itemsSituacao,function(x,item){
                    bodySituacao += '<th class="hidden-xs">'+item.qtd+'</th>';
                    bodySituacao += '<th class="hidden-xs"><span class="hidden-xs">R$</span>'+$.number(item.valor,2)+'</th>';
                    
                    totalizador.itemsSituacao[x][0] += item.qtd;
                    totalizador.itemsSituacao[x][1] += item.valor;
                });
            }

            $('#id_compromisso tbody').append(
                '\
                <tr>\
                    <th>'+obj.title+'</th>\
                    <th><span class="hidden-xs">R$</span> '+$.number(obj.realizado,2)+'</th>\
                    <th class="hidden-xs hidden-sm"><span class="hidden-xs">R$</span> '+$.number(obj.corrigida,2)+'</th>'+bodySituacao+'\
                    <th><span class="hidden-xs">R$</span> '+$.number(obj.medicao,2)+'</th>\
                    <th class="hidden-xs hidden-sm"><span class="hidden-xs">R$</span> '+$.number(obj.valFatorPond,2)+'</th>\
                    <th>'+obj.percent+'%</th>\
                </tr>\
                '
            );

            totalizador.realizado += obj.realizado;
            totalizador.corrigida += obj.corrigida;
            totalizador.medicao += obj.medicao;
            totalizador.meta += obj.meta;
            totalizador.valFatorPond += obj.valFatorPond;
        });

        if(totalizador.meta>0)
            totalizador.percent = (totalizador.realizado/totalizador.meta)*100;

        //Monta totalizador
        var footerSituacao = '';
        if(totalizador.itemsSituacao.length > 0){
            //Monta colunas do cabeçalho para situações
            $.each(totalizador.itemsSituacao,function(x,item){
                footerSituacao += '<th class="hidden-xs">'+item[0]+'</th>';
                footerSituacao += '<th class="hidden-xs"><span class="hidden-xs">R$</span>'+$.number(item[1],2)+'</th>';
            });
        }

        $('.fator-pond').html('\
            <a class="no-action" \
                data-toggle="tooltip" \
                data-placement="top" \
                title="" data-original-title="Fator de cálculo para fechamento"\
            >'+$.number(data.fatorpond,2)+'</a>');
        $('#id_compromisso tfoot').html('');
        $('#id_compromisso tfoot').append(
            '\
            <tr>\
                <th></th>\
                <th class="text-blue"><a href="#" class="btn btn-sm btn-default" target="_blank" id="btnOpClosed"><span class="hidden-xs">R$</span> '+$.number(totalizador.realizado,2)+'</a></th>\
                <th class="hidden-xs hidden-sm"><span class="hidden-xs">R$</span> '+$.number(totalizador.corrigida,2)+'</th>'+footerSituacao+' \
                <th><span class="hidden-xs">R$</span> '+$.number(totalizador.medicao,2)+'</th>\
                <th class="hidden-xs hidden-sm"><span class="hidden-xs">R$</span> '+$.number(totalizador.valFatorPond,2)+'</th>\
                <th>'+$.number(totalizador.percent,2)+'%</th>\
            </tr>\
            '
        );

        var hrefFechadas = '/oportunidade/lista/?frdash=true';
        hrefFechadas += '&'+$('#id-form-filter').serialize();

        var filterReceitas = '';
        $.each($('#id-form-filter').find('.div-dashboard-receitas').find('ul li'),function(i,obj){
            if($(obj).find('.checkinput').hasClass('icon-checked')){
                filterReceitas += '+'+$(obj).find('.checkinput').attr('alt');
            }
        })

        hrefFechadas+= '&receitas='+filterReceitas.substr(1);

        $('#btnOpClosed').attr('href',hrefFechadas);

        /*if(!data.ok){
            $scope.errorParams++;
            $('.panel-pedra').find('.aviso').html('Você precisa se comprometer mais.');
            $('.panel-pedra').find('.messageDash').fadeIn();
        }*/
        $('#id_compromisso thead a').tooltip();
    };

    /**
     * Evento de clique da seta ao lado da data
     *
     * @return void
     */
    $scope.onClickArrowDate = function(){
        event.stopPropagation();
        if($('.div-form-date').is(':visible')){
            $scope.closeFormDate();
        }else{
            $('.div-form-date').css({
                'top': $('#id_arrow_date').offset().top + $('#id_arrow_date').outerHeight(),
                'right': $(window).width() - ($('#id_arrow_date').offset().left + $('#id_arrow_date').outerWidth())
            });
            $('.div-form-date').fadeIn('fast');
            $('#id_arrow_date').css({
                'background':'#ecf0f1',
                'border': 'solid 2px #dce4ec'
            });
        }
    }

    /**
     * Função para fechar o formulário de filtro de datas
     *
     * @return void
     */
    $scope.closeFormDate = function(){
        $('.div-form-date').fadeOut('fast');
        $('#id_arrow_date').css({
            'background':'#fff',
            'border': '0px'
        });
    }

    /**
     * Exibe/Esconde gifs de loading dos charts
     *
     * @return void
     */
    $scope.toggleLoading = function(){
        $('.loading_chart').toggle();
    }

    /**
     * Evento de click no botão de atualizar
     *
     */
    $scope.onClickAtualizar = function(){
        $scope.refreshCharts();

        if($.cookies.test()){
            $.cookies.set("id_visao", $('#id_visao').val(), { path: '/oportunidade/dashboard', expires: 7 });
            $.cookies.set("id_tipo_meta", $('#id_tipo_meta').val(), { path: '/oportunidade/dashboard', expires: 7 });
            $.cookies.set("id_dia_ini", $('#id_dia_ini').val(), { path: '/oportunidade/dashboard', expires: 7 });
            $.cookies.set("id_dia_fim", $('#id_dia_fim').val(), { path: '/oportunidade/dashboard', expires: 7 });

            var receitas = '';
            $.each($('.div-dashboard-receitas ul li a.icon-checked'),function(i,obj){
                receitas+=','+$(obj).html();
            });
            $.cookies.set("id_receitas", receitas.substr(1), { path: '/oportunidade/dashboard', expires: 7 });
        }

        $('#id-ul-filter').fadeOut();
    }

    /**
     * Evento de click do checkbox de receita
     *
     */
    $scope.onClickCheckReceita = function(event){
        event.preventDefault();
        if($(this).hasClass('icon-checked')){
            $(this).removeClass('icon-checked')
            $(this).addClass('icon-unchecked')
        }else{
            $(this).removeClass('icon-unchecked')
            $(this).addClass('icon-checked')
        }
        //$scope.refreshCharts();
        return false;
    }

    /**
     * Evento para abrir formulário de filtro
     *
     * @return void
     */
    $scope.onClickDlDropDown = function(event){
        $('#id-ul-filter').toggle();
    }

    /**
     * Função para setar os parametros com os cookies
     *
     * @return void
     */
    $scope.setCookieFilters = function(){
        if($.cookies.test()){
            var id_visao = $.cookies.get("id_visao");
            var id_tipo_meta = $.cookies.get("id_tipo_meta");
            var id_dia_ini = $.cookies.get("id_dia_ini");
            var id_dia_fim = $.cookies.get("id_dia_fim");
            var id_receitas = $.cookies.get('id_receitas');

            if(typeof id_visao != 'undefined' && id_visao!=null) $('#id_visao').val(id_visao);
            if(typeof id_tipo_meta != 'undefined' && id_tipo_meta!=null) $('#id_tipo_meta').val(id_tipo_meta);
            if(typeof id_dia_ini != 'undefined' && id_dia_ini!=null) $('#id_dia_ini').val(id_dia_ini);
            if(typeof id_dia_fim != 'undefined' && id_dia_fim!=null) $('#id_dia_fim').val(id_dia_fim);

            if(typeof id_receitas != 'undefined' && id_receitas != null){
                $('.div-dashboard-receitas ul li a.icon-checked').removeClass('icon-checked');
                $('.div-dashboard-receitas ul li a').addClass('icon-unchecked');
                var receitas = id_receitas.split(',');
                var receitasStr = '';
                $.each($('.div-dashboard-receitas ul li a'),function(i,obj){
                    $.each(receitas,function(x,item){
                        if(item==$(obj).html()){
                            $(obj).removeClass('icon-unchecked');
                            $(obj).addClass('icon-checked');
                        }
                    });
                });
            }
        }
    }    

    $scope.setCookieFilters();
    $scope.refreshCharts();
    $('.dateField').datepicker(app.datePickerBr);
    $('#dlDropDown').bind('click',$scope.onClickDlDropDown);
    $('html').click(function(event){
        //Tratamento para ui-datepicker não fechar div de filtro
        var elePai = $(event.target).parent();
        while ($(elePai).parent().length > 0) {
            elePai = $(elePai).parent();
        }

        if($(elePai).attr('class')!= 'undefined'){
            if($(elePai).hasClass('ui-corner-all')) {
                event.stopPropagation();
                $(elePai).find('a.ui-corner-all').bind('click',function(e){ e.stopPropagation(); });
            }else{
                if($('#id-ul-filter').is(':visible')){
                    //Testa se objeto clicado não está no botão ou no form
                    if($(event.target).attr('id') != 'id-ul-filter' && $(event.target).attr('id') != 'dlDropDown'){
                        ele = $('#dlDropDown').find(event.target);
                        if(!ele.length>0){
                            ele = $('#id-ul-filter').find(event.target);
                            if(!ele.length>0){
                                $('#id-ul-filter').fadeOut();
                            }
                        }
                    }
                    
                }
            }
        }
    });

    /*
     * Atribui click dos checkbox de receita
     */
    $('.checkinput').bind('click',$scope.onClickCheckReceita);
    //Impede que feche o div do filtro quando houver um click
    $('#id-div-filter').bind('click',function(event){ event.stopPropagation(); });
});