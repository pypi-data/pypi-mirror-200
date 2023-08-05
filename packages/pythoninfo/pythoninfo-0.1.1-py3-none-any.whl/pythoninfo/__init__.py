import itertools
try:
    from importlib.metadata import distributions
except ImportError:
    from importlib_metadata import distributions
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files
import os
import platform
from string import Template
import typing as t


def get_installed_packages() -> t.Dict[str, t.List[t.Tuple[str, str]]]:
    fields = ('Name', 'Version', 'Summary', 'License')
    ignored = {'pip', 'setuptools', 'wheel'}
    result = {}

    for d in sorted(distributions(), key=lambda d: d.metadata['Name'].lower()):
        name = d.metadata['Name']
        if name not in ignored:
            m = d.metadata
            value = [(k, m.get(k, '')) for k in fields]
            value.append((
                'Requires', sorted(m.get_all('Requires-Dist', ()), key=str.lower)
            ))
            value.append((
                'Links', sorted(i.split(', ') for i in m.get_all('Project-URL', ()))
            ))
            result[name] = value

    return result


def get_system_info() -> t.List[t.Tuple[str, str]]:
    """Returns information about the interpreter and OS."""
    return [
        ('Version', platform.python_version()),
        ('System', ' '.join(platform.uname())),
        ('Implementation', platform.python_implementation()),
        ('Build Date', platform.python_build()[1]),
        ('Compiler', platform.python_compiler()),
        ('Scm Branch', platform.python_branch()),
        ('Scm Revision', platform.python_revision()),
        ('Run in Docker', os.path.exists('/.dockerenv')),
    ]


def render_header(value, anchor='') -> str:
    anchor = anchor or f'header_{value}'
    return f'<h2><a id="{anchor}">{value}</a></h2>'


def render_hyperlink(url, text='', target='') -> str:
    text = text or url
    target = target or '_blank'
    return f'<a href="{url}" target="{target}">{text}</a>'


def render_table(rows, headers=None) -> str:
    thead = ''
    tbody = []

    if headers is not None:
        thead = ''.join('<th>%s</th>' % s for s in headers)

    for r in rows:
        tbody.append(
            '<tr>%s</tr>' % ''.join(f'<td>{c}</td>' for c in r)
        )

    tbody = ''.join(tbody)

    return f'<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>'


def render_env_table():
    header = render_header('Environment')
    table = render_table(
        rows=sorted(os.environ.items()),
        headers=('Variable', 'Value')
    )
    return f'{header}{table}'


def render_packages_table():
    installed_packages = get_installed_packages()
    html = []

    for name, m in installed_packages.items():
        rows = []

        for k, v in m:
            if k == 'Requires':
                rows.append(('Requires', '<br>'.join(v)))
            elif k == 'Links':
                rows.extend((text, render_hyperlink(url)) for text, url in v)
            else:
                rows.append((k, v))

        html.extend((
            render_header(name),
            render_table(rows),
        ))

    return ''.join(html)


def render_system_table() -> str:
    packages = ' '.join(
        '<a href="#header_{0}">{0}</a>'.format(name)
        for name in sorted(get_installed_packages(), key=str.lower)
    )
    rows = itertools.chain.from_iterable((
        get_system_info(),
        (('Installed packages', packages),),
    ))
    return render_table(rows)


def render_template(name, **kwargs):
    path = files(__name__).joinpath(f'resources/{name}')
    tmpl = Template(path.read_text())
    return tmpl.substitute(**kwargs)


def pythoninfo():
    return render_template(
        'index.html',
        env_table=render_env_table(),
        packages_table=render_packages_table(),
        system_table=render_system_table(),
        version=platform.python_version(),
    )
