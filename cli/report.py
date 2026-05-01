import click

from database import get_session
import reports


@click.group()
def report():
    """Звіти для адміністратора."""
    pass


@report.command("student")
@click.argument("student_id", type=int)
def report_student(student_id):
    """Успішність учня."""
    with get_session() as session:
        click.echo(reports.report_student(session, student_id))


@report.command("group")
@click.argument("group_id", type=int)
def report_group(group_id):
    """Розклад занять групи."""
    with get_session() as session:
        click.echo(reports.report_group_schedule(session, group_id))


@report.command("summary")
def report_summary():
    """Загальна успішність школи."""
    with get_session() as session:
        click.echo(reports.report_school_summary(session))
