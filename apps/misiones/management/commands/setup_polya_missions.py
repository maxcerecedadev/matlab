from django.core.management.base import BaseCommand
from apps.misiones.models import Mision, Habilidad
import json

class Command(BaseCommand):
    help = 'Replaces active missions with curriculum-aligned Polya missions'

    def handle(self, *args, **kwargs):
        # 1. Clear existing active missions
        deleted_count, _ = Mision.objects.filter(activa=True).delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} active missions.'))

        # 2. Get existing Habilidad
        habilidad = Habilidad.objects.first()
        if not habilidad:
            self.stdout.write(self.style.ERROR('No Habilidad found.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Using Habilidad: {habilidad.nombre} (ID: {habilidad.habilidad_id})'))

        # 3. Define Curriculum-Aligned Missions
        samples = [
            # ===== SUMA =====
            {
                "titulo": "Los Caramelos de Ana",
                "tipo_operacion": "suma",
                "descripcion": "Ana tiene 3 caramelos y le dan 2 más. ¿Cuántos caramelos tiene ahora?",
                "instrucciones_polya": {
                    "Enunciado": "Ana tiene 3 caramelos y le dan 2 más. ¿Cuántos caramelos tiene ahora?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántos caramelos tiene Ana en total?",
                        "datos_conocidos": "Tiene 3 caramelos, le dan 2 más",
                        "condiciones": "Juntar todos los caramelos"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Sumar los dos números",
                        "tactica_sugerida": "Cuenta: 1, 2, 3 (los que tiene), luego 4, 5 (los que le dan)"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "3 + 2 = 5",
                        "operacion_matematica": "3 + 2"
                    },
                    "Fase 4": {
                        "resultado_final": "5",
                        "pregunta_reflexion": "¿Puedes contar con tus dedos? 3 dedos + 2 dedos = 5 dedos"
                    }
                },
                "solucion_correcta": "5",
                "alternativas": ["4", "5", "6"]
            },
            {
                "titulo": "Propiedad Mágica",
                "tipo_operacion": "suma",
                "descripcion": "¿Es igual 6 + 3 que 3 + 6?",
                "instrucciones_polya": {
                    "Enunciado": "¿Es igual 6 + 3 que 3 + 6?",
                    "Fase 1": {
                        "que_se_pide": "¿Dan el mismo resultado?",
                        "datos_conocidos": "Dos sumas: 6+3 y 3+6",
                        "condiciones": "Comparar ambos resultados"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Calcular cada suma",
                        "tactica_sugerida": "Haz las dos sumas y compara"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "6 + 3 = 9, y 3 + 6 = 9",
                        "operacion_matematica": "6+3 y 3+6"
                    },
                    "Fase 4": {
                        "resultado_final": "9",
                        "pregunta_reflexion": "¿Ves? Cambiar el orden no cambia el resultado"
                    }
                },
                "solucion_correcta": "9",
                "alternativas": ["8", "9", "10"]
            },
            {
                "titulo": "Las Canicas de María",
                "tipo_operacion": "suma",
                "descripcion": "María tiene 28 canicas y le regalan 17 canicas más. ¿Cuántas tiene ahora?",
                "instrucciones_polya": {
                    "Enunciado": "María tiene 28 canicas y le regalan 17 canicas más. ¿Cuántas tiene ahora?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas canicas tiene ahora María?",
                        "datos_conocidos": "Tiene 28, le dan 17 más",
                        "condiciones": "Sumar todo"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Suma vertical",
                        "tactica_sugerida": "Suma primero 8+7, luego 20+10"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "8+7=15 (llevo 1), 2+1+1=4. Total: 45",
                        "operacion_matematica": "28 + 17"
                    },
                    "Fase 4": {
                        "resultado_final": "45",
                        "pregunta_reflexion": "¿Si le quitas 17 a 45, te da 28?"
                    }
                },
                "solucion_correcta": "45",
                "alternativas": ["43", "45", "47"]
            },

            # ===== RESTA =====
            {
                "titulo": "Los Soles de Ana",
                "tipo_operacion": "resta",
                "descripcion": "Ana tiene 25 soles. Compra un cuaderno de 9 soles. ¿Cuánto dinero le queda?",
                "instrucciones_polya": {
                    "Enunciado": "Ana tiene 25 soles. Compra un cuaderno de 9 soles. ¿Cuánto dinero le queda?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuánto dinero le queda a Ana?",
                        "datos_conocidos": "Tenía 25 soles, gastó 9",
                        "condiciones": "Restar lo que gastó"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Restar con llevada",
                        "tactica_sugerida": "Del 25, quita 9. Pide prestado si hace falta"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "25-9: Como 5<9, pido prestada 1 decena. 15-9=6, 1-0=1. Total: 16",
                        "operacion_matematica": "25 - 9"
                    },
                    "Fase 4": {
                        "resultado_final": "16",
                        "pregunta_reflexion": "¿Si sumas 16+9 te da 25?"
                    }
                },
                "solucion_correcta": "16",
                "alternativas": ["14", "16", "18"]
            },
            {
                "titulo": "Resta sin Llevar",
                "tipo_operacion": "resta",
                "descripcion": "En el árbol había 45 manzanas. Recogieron 23. ¿Cuántas quedan?",
                "instrucciones_polya": {
                    "Enunciado": "En el árbol había 45 manzanas. Recogieron 23. ¿Cuántas quedan?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas manzanas quedan?",
                        "datos_conocidos": "Había 45, quitaron 23",
                        "condiciones": "Restar las que quitaron"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Resta simple",
                        "tactica_sugerida": "Resta unidades con unidades, decenas con decenas"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "5-3=2, 4-2=2. Total: 22",
                        "operacion_matematica": "45 - 23"
                    },
                    "Fase 4": {
                        "resultado_final": "22",
                        "pregunta_reflexion": "¿Quedan menos manzanas que antes?"
                    }
                },
                "solucion_correcta": "22",
                "alternativas": ["20", "22", "24"]
            },

            # ===== MULTIPLICACIÓN =====
            {
                "titulo": "Las Cajas de María",
                "tipo_operacion": "multiplicacion",
                "descripcion": "María tiene 3 cajas. En cada caja hay 4 caramelos. ¿Cuántos caramelos tiene en total?",
                "instrucciones_polya": {
                    "Enunciado": "María tiene 3 cajas. En cada caja hay 4 caramelos. ¿Cuántos caramelos tiene en total?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántos caramelos tiene María?",
                        "datos_conocidos": "3 cajas, 4 caramelos en cada caja",
                        "condiciones": "Contar todos los caramelos"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Suma repetida o multiplicación",
                        "tactica_sugerida": "Suma 4+4+4 o usa 3×4"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "4+4+4 = 12, o 3×4 = 12",
                        "operacion_matematica": "3 × 4"
                    },
                    "Fase 4": {
                        "resultado_final": "12",
                        "pregunta_reflexion": "¿Si cuentas de 4 en 4 tres veces llegas a 12?"
                    }
                },
                "solucion_correcta": "12",
                "alternativas": ["10", "12", "14"]
            },
            {
                "titulo": "Los Platos de Galletas",
                "tipo_operacion": "multiplicacion",
                "descripcion": "Hay 5 platos y en cada plato hay 2 galletas. ¿Cuántas galletas hay?",
                "instrucciones_polya": {
                    "Enunciado": "Hay 5 platos y en cada plato hay 2 galletas. ¿Cuántas galletas hay?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas galletas hay en total?",
                        "datos_conocidos": "5 platos, 2 galletas por plato",
                        "condiciones": "Contar todas"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Multiplicar",
                        "tactica_sugerida": "Dibuja 5 platos con 2 galletas cada uno"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "5×2 = 10, o 2+2+2+2+2 = 10",
                        "operacion_matematica": "5 × 2"
                    },
                    "Fase 4": {
                        "resultado_final": "10",
                        "pregunta_reflexion": "¿Si sumas todos los 2 te da 10?"
                    }
                },
                "solucion_correcta": "10",
                "alternativas": ["8", "10", "12"]
            },
            {
                "titulo": "Las Pelotas en Cajas",
                "tipo_operacion": "multiplicacion",
                "descripcion": "En cada caja hay 3 pelotas. Si hay 5 cajas, ¿cuántas pelotas hay?",
                "instrucciones_polya": {
                    "Enunciado": "En cada caja hay 3 pelotas. Si hay 5 cajas, ¿cuántas pelotas hay?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas pelotas hay en total?",
                        "datos_conocidos": "3 pelotas por caja, 5 cajas",
                        "condiciones": "Multiplicar"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Usar tabla del 3",
                        "tactica_sugerida": "Suma 5 veces el número 3"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "3×5 = 15, o 3+3+3+3+3 = 15",
                        "operacion_matematica": "3 × 5"
                    },
                    "Fase 4": {
                        "resultado_final": "15",
                        "pregunta_reflexion": "¿Si sumas 5 veces el 3 te da 15?"
                    }
                },
                "solucion_correcta": "15",
                "alternativas": ["13", "15", "17"]
            },

            # ===== DIVISIÓN =====
            {
                "titulo": "Repartir Caramelos",
                "tipo_operacion": "division",
                "descripcion": "Ana tiene 12 caramelos y los reparte entre 3 amigos. ¿Cuántos caramelos recibe cada uno?",
                "instrucciones_polya": {
                    "Enunciado": "Ana tiene 12 caramelos y los reparte entre 3 amigos. ¿Cuántos caramelos recibe cada uno?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántos caramelos recibe cada amigo?",
                        "datos_conocidos": "12 caramelos, 3 amigos",
                        "condiciones": "Repartir en partes iguales"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Dividir",
                        "tactica_sugerida": "Dibuja 3 amigos y reparte uno por uno"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "12÷3 = 4",
                        "operacion_matematica": "12 ÷ 3"
                    },
                    "Fase 4": {
                        "resultado_final": "4",
                        "pregunta_reflexion": "¿Si sumas 4+4+4 te da 12?"
                    }
                },
                "solucion_correcta": "4",
                "alternativas": ["3", "4", "5"]
            },
            {
                "titulo": "Galletas en Bolsas",
                "tipo_operacion": "division",
                "descripcion": "Hay 20 galletas y quieres ponerlas en 4 bolsas. ¿Cuántas galletas van en cada bolsa?",
                "instrucciones_polya": {
                    "Enunciado": "Hay 20 galletas y quieres ponerlas en 4 bolsas. ¿Cuántas galletas van en cada bolsa?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas galletas por bolsa?",
                        "datos_conocidos": "20 galletas, 4 bolsas",
                        "condiciones": "Dividir igual"
                    },
                    "Fase 2": {
                        "estrategia_principal": "División exacta",
                        "tactica_sugerida": "Usa 20÷4"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "20÷4 = 5. Como 5×4=20, no sobra nada",
                        "operacion_matematica": "20 ÷ 4"
                    },
                    "Fase 4": {
                        "resultado_final": "5",
                        "pregunta_reflexion": "¿Si multiplicas 5×4 te da 20?"
                    }
                },
                "solucion_correcta": "5",
                "alternativas": ["4", "5", "6"]
            },
            {
                "titulo": "Canicas en Cajas",
                "tipo_operacion": "division",
                "descripcion": "Luis tiene 15 canicas y quiere repartirlas en 4 cajas. ¿Cuántas canicas van en cada caja y cuántas sobran?",
                "instrucciones_polya": {
                    "Enunciado": "Luis tiene 15 canicas y quiere repartirlas en 4 cajas. ¿Cuántas canicas van en cada caja y cuántas sobran?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas por caja y cuántas sobran?",
                        "datos_conocidos": "15 canicas, 4 cajas",
                        "condiciones": "División inexacta"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Dividir y ver qué sobra",
                        "tactica_sugerida": "Reparte de 1 en 1 hasta que no puedas más"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "15÷4 = 3 (porque 3×4=12). Sobran: 15-12 = 3",
                        "operacion_matematica": "15 ÷ 4"
                    },
                    "Fase 4": {
                        "resultado_final": "3",
                        "pregunta_reflexion": "¿Si pones 3 en cada caja, te sobran 3?"
                    }
                },
                "solucion_correcta": "3",
                "alternativas": ["2", "3", "4"]
            },
            {
                "titulo": "Los Lápices",
                "tipo_operacion": "division",
                "descripcion": "Hay 20 lápices y quieres formar grupos de 5 lápices. ¿Cuántos grupos puedes hacer?",
                "instrucciones_polya": {
                    "Enunciado": "Hay 20 lápices y quieres formar grupos de 5 lápices. ¿Cuántos grupos puedes hacer?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántos grupos se forman?",
                        "datos_conocidos": "20 lápices, grupos de 5",
                        "condiciones": "Agrupar de 5 en 5"
                    },
                    "Fase 2": {
                        "estrategia_principal": "División como agrupación",
                        "tactica_sugerida": "Cuenta de 5 en 5: 5, 10, 15, 20"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "20÷5 = 4 grupos",
                        "operacion_matematica": "20 ÷ 5"
                    },
                    "Fase 4": {
                        "resultado_final": "4",
                        "pregunta_reflexion": "¿Si sumas 5+5+5+5 te da 20?"
                    }
                },
                "solucion_correcta": "4",
                "alternativas": ["3", "4", "5"]
            }
        ]

        # 4. Create Missions
        for data in samples:
            polya_json = json.dumps(data["instrucciones_polya"])
            Mision.objects.create(
                habilidad=habilidad,
                titulo=data["titulo"],
                descripcion=data["descripcion"],
                instrucciones_polya=polya_json,
                tipo_operacion=data["tipo_operacion"],
                activa=True,
                alternativa1=data["alternativas"][0],
                alternativa2=data["alternativas"][1],
                alternativa3=data["alternativas"][2],
                solucion_correcta=data["solucion_correcta"]
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(samples)} curriculum-aligned missions.'))
