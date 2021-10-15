############################ Copyrights and license ############################
#                                                                              #
#                                                                              #
# Copyright 2021 G2V Optics                                                    #
#                                                                              #
#                                                                              #
################################################################################

import setuptools

version = "1.0.0"

if __name__ == "__main__":
    setuptools.setup(
        name="G2VPico",
        version=version,
        description="Python API library for interaction with G2V Optics Pico",
        author="Chris Woloschuk",
        author_email="chris@g2voptics.com",
        url="https://github.com/G2VPico",
        python_requires=">3.6",
    )