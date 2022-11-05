
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.define "RecipeDexVM"
  config.vm.hostname = "dev-vm"
  config.vm.provider :virtualbox do |vb|
	vb.name = "RecipeDexVM"
  end
  
  config.vm.synced_folder ".", "/home/vagrant/RecipeDex"
  config.vm.provision "shell", path: "dev-vm.sh", privileged: true
  config.vm.provision 'shell', reboot: true
end
