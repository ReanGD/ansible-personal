{ config, pkgs, ... }:

{
  services.k3s = {
    enable = true;
    role = "server";
    configPath = config.sops.templates."k3s-conf".path;
  };

  sops.templates."k3s-conf".content = ''
    cluster-init: true
    disable:
      - traefik
      - servicelb
    tls-san:
      - "${config.sops.placeholder."k3s/public_ip"}"
      - "${config.sops.placeholder."k3s/local_ip"}"
    token: "${config.sops.placeholder."k3s/token"}"
    write-kubeconfig-mode: "0644"
    bind-address: "0.0.0.0"
  '';

environment.etc."rancher/k3s/manifests/argocd-installer.yaml".text = ''
    apiVersion: v1
    kind: Namespace
    metadata:
      name: argocd
    ---
    apiVersion: helm.cattle.io/v1
    kind: HelmChart
    metadata:
      name: argocd
      namespace: kube-system
    spec:
      chart: argo-cd
      repo: https://argoproj.github.io/argo-helm
      targetNamespace: argocd
      createNamespace: true
      version: 7.3.4
      valuesContent: |
        configs:
          params:
            server.insecure: true
          secret:
            argocdServerAdminPassword: "${config.sops.placeholder."argocd/admin_password_hash"}"
          repositories:
            cluster-configs:
              url: https://github.com/ReanGD/ansible-personal
        server:
          additionalApplications:
            - name: root-cluster
              namespace: argocd
              project: default
              source:
                repoURL: https://github.com/ReanGD/ansible-personal
                targetRevision: master
                path: argocd
              destination:
                server: https://kubernetes.default.svc
                namespace: argocd
              syncPolicy:
                automated:
                  prune: true
                  selfHeal: true
  '';

  systemd.tmpfiles.rules = [
    "L+ /var/lib/rancher/k3s/server/manifests/argocd-installer.yaml - - - - /etc/rancher/k3s/manifests/argocd-installer.yaml"
  ];

  boot.kernelModules = [ "overlay" "br_netfilter" ];

  networking.firewall = {
    allowedTCPPorts = [
      80    # HTTP
      443   # HTTPS
      6443  # Kubernetes API Server — для удаленного управления через kubectl
      2379  # etcd client — обмен данными между компонентами управления (нужен для HA)
      2380  # etcd peer — взаимодействие между узлами etcd (нужен для HA/cluster-init)
      10250 # Kubelet API — для получения логов и выполнения команд внутри подов
    ];
    allowedUDPPorts = [
      8472  # Flannel VXLAN — необходим для сетевого взаимодействия между подами (CNI)
    ];
  };

  environment.systemPackages = with pkgs; [ k3s kubectl kubernetes-helm argocd ];
  environment.variables.KUBECONFIG = "/etc/rancher/k3s/k3s.yaml";
}
