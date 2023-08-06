graph_patent = {"MAIN_TABLE": "EN_PATENTE",
                "CHECKPOINT": {"DB": "__CVLAC__", "KEYS": ["COD_RH", "COD_PATENTE"]},
                "SCHEMA_VERSION": 0.1,
                "GRAPH": [{"EN_PATENTE": [
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

                    # institucion patentadora(Esta no va a COD_INS para patente)
                    # no tiene sentido el COD, voy a usar ID
                    {"KEYS": ["ID_INST_PATENTADORA/ID_INSTITUCION"],
                     "DB":"__CVLAC__",
                     "TABLES":[{'EN_INSTITUCION/PATENTADORA': [  # EN_INSTITUCION/patenting_institution
                         # pais
                         {"KEYS": ["SGL_PAIS"],
                          "DB":"__CVLAC__",
                          "TABLES":[{'EN_PAIS': None}]},

                     ]}]},
                    # institucion explotadora(Esta no va a COD_INS para patente)
                    # no tiene sentido el COD voy a usar ID
                    {"KEYS": ["COD_INST_CONTR_EXPL/COD_INST"],
                     "DB":"__CVLAC__",
                     "TABLES":[{'EN_INSTITUCION/EXPLOTADORA': [
                         # pais
                         {"KEYS": ["SGL_PAIS"],
                          "DB":"__CVLAC__",
                          "TABLES":[{'EN_PAIS': None}]},

                     ]}]},
                    # Re-Institucion otra
                    {"KEYS": ["COD_RH", "COD_INST_OTRO/COD_INST"],
                     "DB":"__CVLAC__",
                     "TABLES":[{'EN_INSTITUCION_OTRA': None}

                               ]},
                    # prod_tecnica
                    {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                     "DB":"__CVLAC__",
                     "TABLES":[{'EN_PROD_TECNICA': [
                         {"KEYS": ["COD_RH", "COD_PRODUCTO"],
                          "DB":"__CVLAC__",
                          "TABLES":[{"EN_PRODUCTO": None},
                                    {"EN_PROD_EMPRESA_ID": None},
                                    {"EN_PROD_SOFTWARE": None},
                                    {"EN_PROD_VEGETAL": None},
                                    {"EN_PROD_TECNOLOGICO": None},
                                    {"EN_SECRETO_INDUSTRIAL": None},
                                    {"EN_REGISTRO": None},
                                    # Producto Norma
                                    {'EN_PROD_NORMA': [
                                        # Editorial
                                        {"KEYS": ["COD_EDITORIAL"],
                                         "DB":"__CVLAC__",
                                         "TABLES":[{'EN_EDITORIAL': None}]},
                                        # Editorial others
                                        {"KEYS": ["COD_RH", "COD_EDITORIAL_OTRO/COD_EDITORIAL"],
                                         "DB":"__CVLAC__",
                                         "TABLES":[{'EN_EDITORIAL_OTRO': None}]},

                                    ]},

                                    ]}
                     ]}

                    ]},

                ]}
                ]}
