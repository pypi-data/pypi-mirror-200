'''
'''

from duty import duty


__all__ = [
    'clean',
]


@duty
def clean(ctx):
    '''
    Clean up the project directory.
    '''

    ctx.run(
        'rm -rf .html || true',
        title="Remove .html folder"
    )
    ctx.run(
        'rm -f poetry.lock || true',
        title="Remove poetry.lock file"
    )
    ctx.run(
        'rm -rf dist || true',
        title="Remove dist folder"
    )
