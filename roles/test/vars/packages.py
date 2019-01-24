# global host
pkgs = []
grps = []

pkgs += ["python-amqp", "python-hypothesis"]

packages = pkgs
groups = grps
ignore_packages = ["yaourt", "ansible"]
ignore_groups = ["base", "base-devel"]
