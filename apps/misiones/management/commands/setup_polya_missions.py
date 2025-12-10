from django.core.management.base import BaseCommand
from apps.misiones.models import Mision, Habilidad
import json

class Command(BaseCommand):
    help = 'Replaces active missions with Polya-structured sample missions'

    def handle(self, *args, **kwargs):
        # 1. Clear existing active missions
        deleted_count, _ = Mision.objects.filter(activa=True).delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} active missions.'))

        # 2. Get existing Habilidad (to avoid ID insert issues on legacy DB)
        habilidad = Habilidad.objects.first()
        if not habilidad:
            self.stdout.write(self.style.ERROR('No Habilidad found. Cannot create missions without a skill category.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Using Habilidad: {habilidad.nombre} (ID: {habilidad.habilidad_id})'))

        # 3. Define Sample Missions (Polya Structure)
        samples = [
            {
                "titulo": "La Fiesta de Cumpleaños",
                "tipo_operacion": "suma",
                "descripcion": "Juan está organizando su fiesta. Tiene 12 globos rojos y su mamá le compró 15 globos azules. ¿Cuántos globos tiene en total?",
                "instrucciones_polya": {
                    "Enunciado": "Juan está organizando su fiesta. Tiene 12 globos rojos y su mamá le compró 15 globos azules. ¿Cuántos globos tiene en total?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántos globos tiene en total?",
                        "datos_conocidos": "12 globos rojos, 15 globos azules",
                        "condiciones": "Juntar todos los globos"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Suma directa",
                        "tactica_sugerida": "¿Puedes dibujar los globos de cada color y contarlos todos?"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "Tengo un grupo de 12 y otro de 15. Debo unirlos.",
                        "operacion_matematica": "12 + 15"
                    },
                    "Fase 4": {
                        "resultado_final": "27",
                        "pregunta_reflexion": "¿Es lógico que el número final sea mayor que 15?"
                    }
                },
                "solucion_correcta": "27",
                "alternativas": ["25", "27", "30"]
            },
            {
                "titulo": "Repartiendo Galletas",
                "tipo_operacion": "division",
                "descripcion": "La maestra tiene 20 galletas y quiere dárselas a 4 estudiantes en partes iguales. ¿Cuántas galletas recibe cada uno?",
                "instrucciones_polya": {
                    "Enunciado": "La maestra tiene 20 galletas y quiere dárselas a 4 estudiantes en partes iguales. ¿Cuántas galletas recibe cada uno?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas galletas recibe cada estudiante?",
                        "datos_conocidos": "20 galletas, 4 estudiantes",
                        "condiciones": "Repartir en partes iguales"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Reparto equitativo",
                        "tactica_sugerida": "Dibuja 4 niños y ve dando una galleta a cada uno hasta que se acaben."
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "Divido el total de galletas entre la cantidad de niños.",
                        "operacion_matematica": "20 / 4"
                    },
                    "Fase 4": {
                        "resultado_final": "5",
                        "pregunta_reflexion": "Si multiplicas las galletas de cada niño por los 4 niños, ¿te da 20?"
                    }
                },
                "solucion_correcta": "5",
                "alternativas": ["4", "5", "6"]
            },
            {
                "titulo": "El Álbum de Figuras",
                "tipo_operacion": "resta",
                "descripcion": "Sofía necesita 45 figuras para llenar su álbum. Ya pegó 20. ¿Cuántas le faltan?",
                "instrucciones_polya": {
                    "Enunciado": "Sofía necesita 45 figuras para llenar su álbum. Ya pegó 20. ¿Cuántas le faltan?",
                    "Fase 1": {
                        "que_se_pide": "¿Cuántas figuras faltan?",
                        "datos_conocidos": "Total 45 figuras, tiene 20",
                        "condiciones": "Encontrar la diferencia"
                    },
                    "Fase 2": {
                        "estrategia_principal": "Resta / Diferencia",
                        "tactica_sugerida": "¿Cuánto le falta a 20 para llegar a 45?"
                    },
                    "Fase 3": {
                        "desarrollo_paso_a_paso": "Al total necesario le quito las que ya tiene.",
                        "operacion_matematica": "45 - 20"
                    },
                    "Fase 4": {
                        "resultado_final": "25",
                        "pregunta_reflexion": "¿Si sumas las que tiene y las que faltan, te da el total?"
                    }
                },
                "solucion_correcta": "25",
                "alternativas": ["15", "25", "35"]
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

        self.stdout.write(self.style.SUCCESS('Successfully created 3 Polya-structured missions.'))
