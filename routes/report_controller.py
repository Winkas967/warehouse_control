
from flask import Blueprint, request, send_file, jsonify
from datetime import date, datetime
from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from model.report_model import ReportModel
from model.product_model import ProductModel
from utils.auth import login_required

report_route = Blueprint('report_route', __name__)


@report_route.route('/report/pdf', methods=['GET'])
@login_required
def export_pdf():
    try:
        start_date = date.fromisoformat(
            request.args.get('start_date', '')
        )

        end_date = date.fromisoformat(
            request.args.get('end_date', '')
        )

        if start_date > end_date:
            return jsonify({
                "message": "A data inicial não pode ser maior que a final."
            }), 400

        # Busca as movimentações do período
        transactions = ReportModel.get_transactions_by_period(
            start_date, end_date
        )

        # Busca todos os produtos e seus estoques atuais
        products = ProductModel.get_all()

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm
        )

        styles = getSampleStyleSheet()
        elements = []

        # Cabeçalho
        elements.append(
            Paragraph(
                "RELATÓRIO DE ALMOXARIFADO",
                styles['Title']
            )
        )

        elements.append(Spacer(1, 8))

        elements.append(
            Paragraph(
                f"Período: {start_date.strftime('%d/%m/%Y')} "
                f"até {end_date.strftime('%d/%m/%Y')}",
                styles['Normal']
            )
        )

        elements.append(Spacer(1, 15))

        # Resumo das movimentações
        total_entrada = sum(
            t['amount'] for t in transactions
            if t['type'] == 'entrada'
        )

        total_saida = sum(
            t['amount'] for t in transactions
            if t['type'] == 'saida'
        )

        elements.append(
            Paragraph("RESUMO DAS MOVIMENTAÇÕES", styles['Heading2'])
        )

        summary = [
            ["Movimentações", "Entradas", "Saídas", "Saldo movimentado"],
            [
                len(transactions),
                total_entrada,
                total_saida,
                total_entrada - total_saida
            ]
        ]

        summary_table = Table(summary, colWidths=[55*mm, 40*mm, 40*mm, 55*mm])

        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00995d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Produtos e estoque atual
        elements.append(
            Paragraph("PRODUTOS E ESTOQUE ATUAL", styles['Heading2'])
        )

        product_data = [
            ["Produto", "Descrição", "Quantidade atual"]
        ]

        for p in products:
            product_data.append([
                Paragraph(escape(str(p.name or '')), styles['BodyText']),
                Paragraph(escape(str(p.description or '')), styles['BodyText']),
                str(p.amount)
            ])

        product_table = Table(
            product_data,
            colWidths=[65*mm, 125*mm, 45*mm],
            repeatRows=1
        )

        product_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00995d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 7)
        ]))

        elements.append(product_table)
        elements.append(Spacer(1, 20))

        # Histórico de transações
        elements.append(
            Paragraph("HISTÓRICO DE MOVIMENTAÇÕES", styles['Heading2'])
        )

        transaction_data = [
            ["Data/Hora", "Produto", "Colaborador", "Tipo", "Quantidade"]
        ]

        for t in transactions:
            transaction_date = t['date_transaction']

            if isinstance(transaction_date, datetime):
                date_text = transaction_date.strftime('%d/%m/%Y %H:%M')
            else:
                date_text = transaction_date.strftime('%d/%m/%Y')

            transaction_data.append([
                date_text,
                Paragraph(escape(str(t['product_name'])), styles['BodyText']),
                Paragraph(escape(str(t['contributor_name'])), styles['BodyText']),
                t['type'].upper(),
                str(t['amount'])
            ])

        if not transactions:
            transaction_data.append([
                "-", "Nenhuma movimentação no período", "-", "-", "-"
            ])

        transaction_table = Table(
            transaction_data,
            colWidths=[35*mm, 65*mm, 65*mm, 35*mm, 30*mm],
            repeatRows=1
        )

        transaction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00995d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 7)
        ]))

        elements.append(transaction_table)

        doc.build(elements)

        buffer.seek(0)

        filename = (
            f"relatorio_almoxarifado_"
            f"{start_date}_{end_date}.pdf"
        )

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except ValueError:
        return jsonify({
            "message": "Informe datas válidas."
        }), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500
