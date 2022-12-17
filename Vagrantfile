
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.define "RecipeDexVM"
  config.vm.hostname = "dev-vm"
  
  config.vm.provider :virtualbox do |vb|
    vb.memory = 8192
    vb.cpus = 2
	vb.name = "RecipeDexVM"
	vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/.", "1"]
  end
  
  config.vm.synced_folder ".", "/home/vagrant/RecipeDex"
  config.vm.provision "shell", path: "scripts/setup.sh", privileged: true
  config.vm.provision "shell", reboot: true
end
