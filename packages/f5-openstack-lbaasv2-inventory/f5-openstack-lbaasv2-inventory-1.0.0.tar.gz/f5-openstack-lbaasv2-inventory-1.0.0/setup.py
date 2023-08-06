import neutron_lbaas_inventory
import setuptools

setuptools.setup(
    version=neutron_lbaas_inventory.__version__,
    name="f5-openstack-lbaasv2-inventory",
    description = ("F5 Networks device inventory for OpenStack services"),
    license = "Apache License, Version 2.0",
    author="F5 Networks",
    author_email="openstack@f5.com",
    classifiers=[
        "Environment :: OpenStack",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
    ],
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*", "test*", "test"]),
    entry_points={
        "neutron.db.alembic_migrations":
            "neutron-lbaas-inventory = neutron_lbaas_inventory.db.migration:alembic_migrations",
        "neutron.service_plugins":
            "lbaas_device = neutron_lbaas_inventory.plugins.lbaasdevice:LbaasDevicePlugin"
    },
    data_files=[
        ('/etc/neutron/policy.d', ['etc/neutron/policy.d/lbaas_device.json'])
    ]
)
