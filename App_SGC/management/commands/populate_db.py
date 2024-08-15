from django.core.management.base import BaseCommand
from App_SGC.models import CustomCondominio, CustomCondomino, CustomBloco, FinanceiroEstrutura

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Create CustomCondominio instances
        condominio1, created1 = CustomCondominio.objects.get_or_create(
            n_condominio=1,
            defaults={'nome_condominio': 'Riviera dei Fiori'}
        )
        if created1:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomCondominio: Riviera dei Fiori'))

        condominio2, created2 = CustomCondominio.objects.get_or_create(
            n_condominio=2,
            defaults={'nome_condominio': 'Alameda dos Eucaliptos'}
        )
        if created2:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomCondominio: Alameda dos Eucaliptos'))

        # Create CustomCondomino instances
        condomino1, created3 = CustomCondomino.objects.get_or_create(
            cpf_condomino='22760369153',
            defaults={
                'nome_condomino': 'João Augusto',
                'data_nascimento_condomino': '1980-01-01',
                'telefone_condomino': '981079109',
                'celular_condomino': '981079109',
                'email_condomino': 'joao@yahoo.com.br',
                'data_aquisicao_imovel': '2010-01-01',
                'n_condominio': condominio1
            }
        )
        if created3:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomCondomino: João Augusto'))

        condomino2, created4 = CustomCondomino.objects.get_or_create(
            cpf_condomino='17102234805',
            defaults={
                'nome_condomino': 'Claudia Araujo',
                'data_nascimento_condomino': '1985-05-05',
                'telefone_condomino': '982933310',
                'celular_condomino': '982933310',
                'email_condomino': 'claudiaatavares@yahoo.com.br',
                'data_aquisicao_imovel': '2015-05-05',
                'n_condominio': condominio2
            }
        )
        if created4:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomCondomino: Claudia Araujo'))

        # Create CustomBloco instances
        bloco1, created5 = CustomBloco.objects.get_or_create(
            bloco='B',
            n_condominio=condominio1
        )
        if created5:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomBloco: B'))

        bloco2, created6 = CustomBloco.objects.get_or_create(
            bloco='C',
            n_condominio=condominio2
        )
        if created6:
            self.stdout.write(self.style.SUCCESS('Successfully created CustomBloco: C'))

        # Create FinanceiroEstrutura instances
        root, created7 = FinanceiroEstrutura.objects.get_or_create(
            nome='Receitas',
            n_condominio=condominio1
        )
        if created7:
            self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Receitas'))

        receitas_or = FinanceiroEstrutura.objects.get_or_create(
            nome='Receitas Ordinarias',
            parent=root,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Receitas Ordinarias'))

        taxa_agua = FinanceiroEstrutura.objects.get_or_create(
            nome='Taxa Agua',
            parent=receitas_or,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Taxa Agua'))

        adicional = FinanceiroEstrutura.objects.get_or_create(
            nome='Adicional',
            parent=taxa_agua,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Adicional'))

        teste1 = FinanceiroEstrutura.objects.get_or_create(
            nome='Teste1',
            parent=adicional,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Teste1'))

        taxas_or = FinanceiroEstrutura.objects.get_or_create(
            nome='Taxas Ordinárias',
            parent=receitas_or,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Taxas Ordinárias'))

        reserva_espaco = FinanceiroEstrutura.objects.get_or_create(
            nome='Reserva de Espaço',
            parent=receitas_or,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Reserva de Espaço'))

        fundo_garantia = FinanceiroEstrutura.objects.get_or_create(
            nome='Fundo Garantia',
            parent=root,
            n_condominio=condominio1
        )[0]
        self.stdout.write(self.style.SUCCESS('Successfully created FinanceiroEstrutura: Fundo Garantia'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
