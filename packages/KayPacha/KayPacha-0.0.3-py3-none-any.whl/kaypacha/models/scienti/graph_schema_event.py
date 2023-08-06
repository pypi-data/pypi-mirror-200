
graph_event = {"MAIN_TABLE": "EN_EVENTO",
               "CHECKPOINT": {"DB": "__CVLAC__", "KEYS": ["COD_RH", "COD_EVENTO"]},
               "SCHEMA_VERSION": 0.1,
               "GRAPH": [{"EN_EVENTO": [
                   # autor registrante
                   {"KEYS": ["COD_RH"],
                    "DB":"__CVLAC__",
                    "TABLES":[{'EN_RECURSO_HUMANO': [
                        # municipio
                        {"KEYS": ["COD_RH_MUN_NACIM/COD_RH_MUNICIPIO", "COD_MUN_NACIM/COD_MUNICIPIO"],
                              "DB":"__CVLAC__",
                              "TABLES":[{'EN_MUNICIPIO': [
                                  # departamento
                                  {"KEYS": ["SGL_PAIS", "SGL_DEPARTAMENTO"],
                                   "DB":"__CVLAC__",
                                   "TABLES":[{'EN_DEPARTAMENTO': [
                                       # pais
                                       {"KEYS": ["SGL_PAIS"],
                                        "DB":"__CVLAC__",
                                        "TABLES":[{'EN_PAIS': None}]},

                                   ]}]},
                              ]}]},
                        # level of studies
                        {"KEYS": ["COD_NIVEL_FORMACION"],
                         "DB":"__CVLAC__",
                              "TABLES":[{'EN_NIVEL_FORMACION': None}]},
                    ]},
                   ]},

                   # institucion registrante
                   {"KEYS": ["COD_INST_AVALA/COD_INST"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'EN_INSTITUCION': [
                           # pais
                           {"KEYS": ["SGL_PAIS"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_PAIS': None}]},

                       ]}]},
                   # Re-Institucion
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_INSTITUCION_EVENTO': [
                           # instituciones
                           {"KEYS": ["COD_RH", "COD_INSTITUCION/COD_INST"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_INSTITUCION_OTRA': None}
                                      ]}
                       ]}

                   ]},
                   # Re-Autor otros
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_RH_O_EVENTO': [
                           # Autores otros
                           {"KEYS": ["COD_RH/COD_RH_CREA", "COD_RH_OTRO"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_RECURSO_HUMANO_OTRO': None}
                                      ]}

                       ]}

                   ]},
                   # Re-Comunidad
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_EVENTO_COMUNIDAD':
                                  [
                                      # Comunidad
                                      {"KEYS": ["COD_RH", "COD_COMUNIDAD"],
                                       "DB":"__CVLAC__",
                                       "TABLES":[{'EN_COMUNIDAD': [
                                           # Municipio
                                           {"KEYS": ["COD_RH_MUNICIPIO", "COD_MUNICIPIO"],
                                            "DB":"__CVLAC__",
                                            "TABLES":[{'EN_MUNICIPIO': None}]},
                                           # Re-proyecto comunidad
                                           {"KEYS": ["COD_RH", "COD_COMUNIDAD"],
                                            "DB":"__CVLAC__",
                                            "TABLES":[{'RE_PROYECTO_COMUNIDAD': [
                                                # proyecto
                                                {"KEYS": ["COD_RH", "COD_PROYECTO"],
                                                 "DB":"__CVLAC__",
                                                 "TABLES":[{"EN_PROYECTO": None}]}
                                            ]}]},
                                           # Re-producto comunidad
                                           {"KEYS": ["COD_RH", "COD_COMUNIDAD"],
                                            "DB":"__CVLAC__",
                                            "TABLES":[{'RE_PRODUCTO_COMUNIDAD': [
                                                # producto
                                                {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                                                 "DB":"__CVLAC__",
                                                 "TABLES":[{"EN_PRODUCTO": None}]}
                                            ]}]},

                                       ]}
                                      ]},

                                  ]}
                                 ]},

                   # Re-Grupo
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__GRUPLAC__",
                       "TABLES":[{'RE_GRUPO_RH_EVENTO': [
                           # Grupo
                           {"KEYS": ["NRO_ID_GRUPO"],
                            "DB":"__GRUPLAC__",
                            "TABLES":[{"EN_GRUPO_PESQUISA": [
                                # re_institucion
                                {"KEYS": ["NRO_ID_GRUPO"],
                                 "DB":"__GRUPLAC__",
                                 "TABLES":[{'RE_GRUPO_INSTITUCION': [
                                     # institucion
                                     {"KEYS": ["COD_INST"],
                                      "DB":"__CVLAC__",
                                      "TABLES":[{'EN_INSTITUCION': None}
                                                ]}
                                 ]}
                                ]},
                                # Area reconocimiento level 2 (tiene 3 niveles máximo) (es con COD_RH_AREA???)
                                {"KEYS": ['COD_RH_AREA/COD_RH', 'COD_AREA_CONHEC/COD_AREA_CONOCIMIENTO'],
                                 "DB":"__CVLAC__",
                                 "TABLES":[
                                    {"EN_AREA_CONOCIMIENTO": [
                                        # Area reconocimiento level 1
                                        {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                         "DB":"__CVLAC__",
                                         "TABLES":[{'EN_AREA_CONOCIMIENTO': [
                                             # Area reconocimiento level 0
                                             {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                              "DB":"__CVLAC__",
                                              "TABLES":[{'EN_AREA_CONOCIMIENTO': None}]},
                                         ]}
                                        ]},

                                    ]}
                                ]},
                            ]},
                           ]}
                       ]}

                   ]},
                   # Re-Palabra clave
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_EVENTO_PALABRA_CLA': [
                           # Palabra clave
                           {"KEYS": ["COD_RH", "COD_PALABRA_CLAVE"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_PALABRA_CLAVE': None}
                                      ]}
                       ]}

                   ]},

                   # Re-evento producto
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_PRODUCTO_EVENTO': [
                           # producto  (aca muere por que producto es tabla principal)
                           {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_PRODUCTO': None}
                                      ]}
                       ]}
                   ]},

                   # Re-evento Area de conocimiento
                   {"KEYS": ["COD_RH/COD_RH_EVENTO", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[
                           {'RE_EVENTO_AREA_CON': [
                               # producto  (aca muere por que producto es tabla principal)
                               {"KEYS": ["COD_RH_AREA_CON/COD_RH", "COD_AREA_CONOCIMIENTO"],
                                "DB":"__CVLAC__",
                                "TABLES":[
                                # Area reconocimiento level 2 (tiene 3 niveles máximo)
                                {"EN_AREA_CONOCIMIENTO": [
                                    # Area reconocimiento level 1
                                    {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                        "DB":"__CVLAC__",
                                        "TABLES":[{'EN_AREA_CONOCIMIENTO': [
                                            # Area reconocimiento level 0
                                            {"KEYS": ['COD_RH_PADRE/COD_RH', "COD_AREA_PADRE/COD_AREA_CONOCIMIENTO"],
                                             "DB":"__CVLAC__",
                                             "TABLES":[{'EN_AREA_CONOCIMIENTO': None}]},
                                        ]}
                                    ]},

                                ]}
                               ]}
                           ]}
                   ]},
                   # Re-Sector Apliación
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                       "DB":"__CVLAC__",
                       "TABLES":[{'RE_EVENTO_SECTOR_APL': [
                           # sector aplicación nivel 2
                           {"KEYS": ["COD_SECTOR_APLICACION"],
                            "DB":"__CVLAC__",
                            "TABLES":[{'EN_SECTOR_APLICACION': [
                                # sector aplicación nivel 1
                                {"KEYS": ["COD_SECT_APLIC_PADRE/COD_SECTOR_APLICACION"],
                                 "DB":"__CVLAC__",
                                 "TABLES":[{'EN_SECTOR_APLICACION': None}
                                           ]}
                            ]}
                           ]}
                       ]}

                   ]},
                   # Proyecto directo de evento
                   {"KEYS": ["COD_RH", "COD_EVENTO"],
                    "DB":"__CVLAC__",
                         "TABLES":[{'RE_EVENTO_PROYECTO':
                                    [{"KEYS": ["COD_RH", "COD_PROYECTO"],
                                      "DB":"__CVLAC__",
                                      "TABLES":[{'EN_PROYECTO': None}]},

                                     ]}]},
                   # Proyecto tipo
                   {"KEYS": ["TPO_EVENTO"],
                    "DB":"__CVLAC__",
                    "TABLES":[{'EN_TIPO_EVENTO': None}]},

               ]}
               ]}
