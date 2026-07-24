import datetime
from typing import List, Tuple, Dict

class RelogScheduler:
    """
    Gerencia a lógica de agendamento de Auto-Relog do Legend Online.
    - Evita relog durante horários de eventos fixos (11:00, 13:00, 15:00, 17:00, 19:00, 21:35).
    - Dispara o relog preventivo 15 minutos antes dos eventos.
    - Nos demais horários, segue o intervalo padrão de 2 horas (120 min).
    """

    # Horários e nomes oficiais dos eventos no jogo
    EVENTS: List[Dict[str, str]] = [
        {"time": "11:00", "name": "C.G da manhã"},
        {"time": "12:00", "name": "Arena"},
        {"time": "13:00", "name": "C.B"},
        {"time": "15:00", "name": "C.B"},
        {"time": "17:00", "name": "C.B"},
        {"time": "18:00", "name": "Arena/Arena Guarda"},
        {"time": "19:00", "name": "C.B"},
        {"time": "21:35", "name": "C.G da Noite"},
    ]

    # Compatibilidade legada
    EVENT_TIMES: List[str] = [e["time"] for e in EVENTS]

    # Minutos de antecedência antes do evento para o relog preventivo
    PRE_EVENT_OFFSET_MINS: int = 15

    @classmethod
    def get_pre_event_times(cls) -> List[datetime.time]:
        """Retorna os horários exatos de disparo pré-evento (15 minutos antes)."""
        pre_times = []
        for ev in cls.EVENTS:
            h, m = map(int, ev["time"].split(":"))
            dt = datetime.datetime.combine(datetime.date.today(), datetime.time(h, m))
            dt_pre = dt - datetime.timedelta(minutes=cls.PRE_EVENT_OFFSET_MINS)
            pre_times.append(dt_pre.time())
        return pre_times

    @classmethod
    def calculate_next_relog_seconds(cls, default_interval_mins: int = 120) -> Tuple[int, str]:
        """
        Calcula quantos segundos faltam para o próximo aviso de evento ou intervalo.
        Retorna (segundos_ate_relog, descricao_do_motivo).
        """
        now = datetime.datetime.now()
        today = now.date()

        # 1. Verifica horários pré-evento para o dia de hoje e amanhã
        pre_event_dts = []
        for ev in cls.EVENTS:
            t_str = ev["time"]
            ev_name = ev["name"]
            h, m = map(int, t_str.split(":"))
            event_dt = datetime.datetime.combine(today, datetime.time(h, m))
            pre_dt = event_dt - datetime.timedelta(minutes=cls.PRE_EVENT_OFFSET_MINS)
            
            # Se o disparo de hoje já passou ou falta menos de 10 segundos, calcula para o dia seguinte
            if pre_dt <= (now + datetime.timedelta(seconds=10)):
                pre_dt += datetime.timedelta(days=1)
            pre_event_dts.append((pre_dt, ev_name, t_str))

        # Encontra o disparo pré-evento mais próximo
        next_pre_event_dt, event_name, event_time = min(pre_event_dts, key=lambda x: x[0])
        secs_to_pre_event = max(10, int((next_pre_event_dt - now).total_seconds()))

        # 2. Compara com o intervalo padrão (2 horas = 7200 segundos)
        default_secs = default_interval_mins * 60

        if secs_to_pre_event < default_secs:
            return secs_to_pre_event, f"Evento '{event_name}' (às {event_time})"
        else:
            return default_secs, f"Intervalo de rotina ({default_interval_mins} min)"

