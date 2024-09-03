from setuptools import setup

setup(
    name='simpub',
    version='0.1',
    install_requires=["zmq", "trimesh", "pillow", "numpy", "scipy", "colorama"],
    include_package_data=True,
    packages=['simpub', 'simpub.parser', 'simpub.sim', 'simpub.core', 'simpub.xr_device']
)
