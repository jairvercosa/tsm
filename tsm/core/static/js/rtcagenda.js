/**
 * Rotinas para controle da agenda
 */
var rtcAgenda = {
    /**
     * @var fullCalendar calendar
     */
    calendar: null,

    /**
     * Função onRead da página
     *
     * @return void
     */
    onReady: function(){
        rtcAgenda.refreshCalendar();
        $('#id_visao').on('change',rtcAgenda.onChangeVisao);
    },

    /**
     * Recarrega calendário
     *
     * @return void
     */
    refreshCalendar: function(){
        if(rtcAgenda.calendar != null){
            $(rtcAgenda.calendar).fullCalendar('destroy');
        }
        $('.loading').show();

        rtcAgenda.calendar = $('#calendar').fullCalendar({
            lang: 'pt-br',
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            defaultDate: hoje,
            timeFormat: 'H(:mm)',
            editable: true,
            events: {
                url: '/oportunidade/rtc/data/',
                type: 'GET',
                data: { usuario: $('#id_visao').val() },
                error: function() {
                    alert('Falha na busca dos eventos');
                },
                color: 'yellow',   // a non-ajax option
                textColor: 'black' // a non-ajax option
            },
            eventRender: function (event, element) {
                $(element).attr('href', 'javascript:void(0);');
                $(element).bind('click', function(){
                    $.get(
                        '/oportunidade/rtc/evento/'+event.id+'/',
                        function(response){
                            $('#mdl_event').html(response);
                            $('#mdl_event').modal();
                        }
                    );
                });
            }
        });
        $('.loading').hide();
    },

    /**
     * Evento para mudança de visão
     *
     * @return void
     */
    onChangeVisao: function(){
        rtcAgenda.refreshCalendar();
    }

}
$(document).ready(function(){ rtcAgenda.onReady(); });