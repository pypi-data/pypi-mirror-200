graph_project = {
    "MAIN_TABLE": "SIIU_PROYECTO",
    "CHECKPOINT": {"DB": "BUPP", "KEYS": ["CODIGO"]},
    "SCHEMA_VERSION": 0.1,
    "GRAPH":[
        {
            "SIIU_PROYECTO":[

                {
                    "KEYS": ["CODIGO/PROYECTO"],
                    "DB":"BUPP",
                    "TABLES":[
                        {
                            "SIIU_COMPROMISO_POR_PROYECTO": [
                                {
                                    "KEYS": ["COMPROMISO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_COMPROMISO": None}
                                    ]
                                }
                            ]
                        },
                        {
                            "SIIU_ESTADO_PROYECTO": [
                                {
                                    "KEYS": ["DOCUMENTO_SOPORTE/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_DOCUMENTO_SOPORTE": None}
                                    ]
                                }
                            ]
                        },
                        {
                            "SIIU_AVAL_APROBACION": [
                                {
                                    "KEYS": ["DOCUMENTO_SOPORTE/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_DOCUMENTO_SOPORTE": None}
                                    ]
                                }
                            ]
                        },
                        {"SIIU_ACTUALIZACION_PROYECTO": None},
                        {
                            "SIIU_EVALUACION_TECNICA": [
                                {
                                    "KEYS": ["ETAPA_PROCESO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_ETAPA_PROCESO_SELECCION": None}
                                    ]
                                }
                            ]
                        },
                        {
                            "SIIU_EVALUACION_CIENTIFICA": [
                                {
                                    "KEYS": ["EVALUADOR/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {
                                            "SIIU_EVALUADOR_RECOMENDADO": [
                                                {
                                                    "KEYS": ["EVALUADOR/IDENTIFICADOR"],
                                                    "DB":"BUPP",
                                                    "TABLES": [
                                                        {"SIIU_EVALUADOR": None}
                                                    ]
                                                }
                                            ]
                                        }
                                    ]  
                                }
                            ]
                        },
                        {
                            "SIIU_PARTICIPANTE_PROYECTO": [
                                {
                                    "KEYS": ["PERSONA_NATURAL/IDENTIFICACION"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_PERSONA_NATURAL": None}
                                    ]
                                },
                                {
                                    "KEYS": ["ROL_PARTICIPANTE_PROYECTO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES":[
                                        {"SIIU_ROL_PARTICIPANTE_PROYECTO": None}
                                    ]
                                },
                                {
                                    "KEYS": ["GRUPO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES":[
                                        {"SIIU_GRUPO": None}
                                    ]
                                }
                            ]

                        },
                        {
                            "SIIU_APORTANTE_PROYECTO": [
                                {
                                    "KEYS": ["PERSONA_JURIDICA/NIT"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_PERSONA_JURIDICA": None}
                                    ]
                                    
                                },
                                {
                                    "KEYS": ["GRUPO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_GRUPO": None}
                                    ]
                                },
                                {
                                    "KEYS": ["IDENTIFICADOR/APORTANTE"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_SEGUIMIENTO_APORTANTE": None},
                                        {"SIIU_SEGUIMIENTO_PRESUPUESTO": None}
                                    ]
                                },
                                {
                                    "KEYS": ["IDENTIFICADOR/APORTANTE_PROYECTO"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {
                                            "SIIU_MODIFICACION_PRESUPUESTAL": [
                                                {
                                                    "KEYS": ["IDENTIFICADOR/MODIFICACION_PRESUPUESTAL"],
                                                    "DB":"BUPP",
                                                    "TABLES": [
                                                        {"SIIU_DETALLE_MODIF_PPTAL": None}
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        },
                        {
                            "SIIU_TEXTO_DESCRIPTIVO": [
                                {
                                    "KEYS": ["TEXTO_SOLICITADO/IDENTIFICADOR"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SIIU_TEXTO_SOLICITADO": None}
                                    ]
                                }
                            ]
                        },
                        {"SIIU_SEGUIMIENTO_PPTO_INICIAL": None},
                        {
                            "SMAP_SOLICITUD_ADM": [
                                {
                                    "KEYS": ["ID/ID_SOLICITUD_ADM"],
                                    "DB":"BUPP",
                                    "TABLES": [
                                        {"SMAP_SOL_ADICION_PRESUPUESTAL": None},
                                        {"SMAP_SOLICITUD_CAMBIO_RUBRO": None}
                                    ]
                                }
                            ]
                        }
                    ]
            
                },
                {
                    "KEYS": ["CODIGO/CODIGO_PROYECTO"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_ETAPA_PROYECTO": None}
                    ]
                },
                {
                    "KEYS": ["CLASE_PROYECTO/IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_CLASE_PROYECTO": None}
                    ]
                },
                {
                    "KEYS": ["NIVEL_PROYECTO/IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_NIVEL_PROYECTO": None}
                    ]
                },
                {
                    "KEYS": ["SUBNIVEL_PROYECTO"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_SUBNIVEL_PROYECTO": None}
                    ]
                },
                {
                    "KEYS": ["TIPO_PROYECTO_MACRO/IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_TIPO_PROYECTO": None}
                    ]
                },
                {
                    "KEYS": ["SUBTIPO_PROYECTO/IDENTIFICADOR"],
                    "DB":"BUPP",
                    "TABLES":[
                        {"SIIU_SUBTIPO_PROYECTO": None}
                    ]
                }
            ]
        }
    ]
}
