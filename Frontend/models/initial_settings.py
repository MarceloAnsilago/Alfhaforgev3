from dataclasses import dataclass


@dataclass(frozen=True)
class InitialSettingsOptions:
    mercados: list[str]
    tipos_operacionais: list[str]
    modos_processamento: list[str]
    sim_nao: list[str]
    tempos_graficos: list[str]


def build_initial_settings_options() -> InitialSettingsOptions:
    return InitialSettingsOptions(
        mercados=["B3", "Forex"],
        tipos_operacionais=["Day trade", "Swing trade"],
        modos_processamento=["Cada tick", "Cada segundo"],
        sim_nao=["Nao", "Sim"],
        tempos_graficos=[
            "Corrente",
            "M1",
            "M2",
            "M3",
            "M4",
            "M5",
            "M6",
            "M10",
            "M12",
            "M15",
            "M30",
            "H1",
            "H2",
            "H3",
            "H4",
            "H6",
            "H8",
            "H12",
            "D1",
            "W1",
            "MN1",
        ],
    )
