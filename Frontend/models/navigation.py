from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationItem:
    item_id: str
    label: str
    short_label: str
    icon: str
    description: str


def build_navigation_items() -> list[NavigationItem]:
    return [
        NavigationItem("inf_iniciais", "Inf. Iniciais", "01", "[I]", "Base inicial do projeto e configuracao principal."),
        NavigationItem("stop_loss", "Stop Loss", "02", "[S]", "Stop loss fixo, calculo e protecao por perda."),
        NavigationItem("stop_movel", "Stop Movel", "03", "[M]", "Regras para mover o stop automaticamente."),
        NavigationItem("take_profit", "Take Profit", "04", "[T]", "Take profit fixo, calculo e projecao de lucro."),
        NavigationItem("break_even", "Break Even", "05", "[B]", "Break even e protecao sem prejuizo."),
        NavigationItem("trailing_stop", "Trailing Stop", "06", "[R]", "Trailing stop e acompanhamento dinamico."),
        NavigationItem("saidas_parciais", "Saidas Parciais", "07", "[P]", "Saidas fracionadas e gerenciamento parcial."),
        NavigationItem("sinais", "Sinais", "08", "[N]", "Gatilhos e filtros de sinal."),
        NavigationItem("ajustes_finais", "Ajustes Finais", "09", "[A]", "Acabamento final da estrategia."),
        NavigationItem("montagem", "Montagem", "10", "[G]", "Espaco reservado para o fluxo de montagem da estrategia."),
        NavigationItem("execucao", "Execucao", "11", "[E]", "Fluxo operacional da estrategia, disparo e integracoes."),
        NavigationItem("painel", "Painel", "12", "[L]", "Visualizacao consolidada do painel e controles finais."),
    ]
