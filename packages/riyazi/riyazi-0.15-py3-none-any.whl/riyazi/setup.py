
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('riyazi', parent_package, top_path)
    config.add_subpackage('algebra')
    config.add_subpackage('constants')
    config.add_subpackage('crypto')
    config.add_subpackage('fft')
    config.add_subpackage('geometry')
    config.add_subpackage('integrate')
    config.add_subpackage('interpolate')
    config.add_subpackage('linalg')
    config.add_subpackage('math')
    config.add_subpackage('ndimage')
    config.add_subpackage('odr')
    config.add_subpackage('optimize')
    config.add_subpackage('physics')
    config.add_subpackage('polynomial')
    config.add_subpackage('series')
    config.add_subpackage('signal')
    config.add_subpackage('sparse')
    config.add_subpackage('spatial')
    config.add_subpackage('special')
    
    
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup

    config = configuration(top_path='').todict()
    setup(**config)