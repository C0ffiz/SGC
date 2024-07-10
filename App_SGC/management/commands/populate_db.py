from django.core.management.base import BaseCommand
from App_SGC.models import CustomCondominio, CustomCondomino, CustomBloco

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Insert rows into CustomCondominio
        condominio1 = CustomCondominio.objects.create(n_condominio=1, nome_condominio='Riviera dei Fiori')
        condominio2 = CustomCondominio.objects.create(n_condominio=2, nome_condominio='Alameda dos Eucaliptos')
        
        # Insert rows into CustomCondomino
        CustomCondomino.objects.create(
            cpf_condomino='22760369153', 
            nome_condomino='João Augusto',
            data_nascimento_condomino='1980-01-01',
            bloco='C', 
            apartamento='1501',
            telefone_condomino='981079109',
            celular_condomino='981079109',
            email_condomino='joao@yahoo.com.br',
            data_aquisicao_imovel='2010-01-01',
            n_condominio=condominio1
        )

        CustomCondomino.objects.create(
            cpf_condomino='17102234805', 
            nome_condomino='Claudia Araujo',
            data_nascimento_condomino='1985-05-05',
            bloco='B', 
            apartamento='1502',
            telefone_condomino='982933310',
            celular_condomino='982933310',
            email_condomino='claudiaatavares@yahoo.com.br',
            data_aquisicao_imovel='2015-05-05',
            n_condominio=condominio2
        )

        # Insert rows into CustomBloco
        CustomBloco.objects.create(bloco='B', n_condominio=condominio1)
        CustomBloco.objects.create(bloco='C', n_condominio=condominio2)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
