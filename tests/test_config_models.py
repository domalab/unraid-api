"""Tests for the config models."""
import pytest
from pydantic import ValidationError

from unraid_api.models.config import (CPUConfig, DisplayConfig, DockerConfig,
                                      DynamicDNSConfig, EmailConfig, FTPConfig,
                                      MemoryConfig, MutationResponse,
                                      NetworkConfig, NetworkInterface,
                                      NotificationAgents, NotificationsConfig,
                                      PluginConfig, PushoverConfig,
                                      ShareConfig, SharesConfig, SystemConfig,
                                      TunableConfig, UpdatesConfig, VMConfig)


def test_network_interface():
    """Test NetworkInterface model."""
    data = {
        "name": "eth0",
        "mac": "00:11:22:33:44:55",
        "ip": "192.168.1.100",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "up": True,
        "speed": 1000,
        "duplex": "full"
    }

    model = NetworkInterface(**data)

    assert model.name == "eth0"
    assert model.mac == "00:11:22:33:44:55"
    assert model.ip == "192.168.1.100"
    assert model.netmask == "255.255.255.0"
    assert model.gateway == "192.168.1.1"
    assert model.up is True
    assert model.speed == 1000
    assert model.duplex == "full"


def test_network_interface_minimal():
    """Test NetworkInterface model with minimal data."""
    data = {
        "name": "eth0",
        "mac": "00:11:22:33:44:55",
        "up": True
    }

    model = NetworkInterface(**data)

    assert model.name == "eth0"
    assert model.mac == "00:11:22:33:44:55"
    assert model.ip is None
    assert model.netmask is None
    assert model.gateway is None
    assert model.up is True
    assert model.speed is None
    assert model.duplex is None


def test_network_config():
    """Test NetworkConfig model."""
    data = {
        "interfaces": [
            {
                "name": "eth0",
                "mac": "00:11:22:33:44:55",
                "up": True
            }
        ],
        "dnsServers": ["8.8.8.8", "8.8.4.4"],
        "hostname": "unraid-server"
    }

    model = NetworkConfig(**data)

    assert len(model.interfaces) == 1
    assert model.interfaces[0].name == "eth0"
    assert model.interfaces[0].mac == "00:11:22:33:44:55"
    assert model.interfaces[0].up is True
    assert model.dnsServers == ["8.8.8.8", "8.8.4.4"]
    assert model.hostname == "unraid-server"


def test_cpu_config():
    """Test CPUConfig model."""
    data = {
        "model": "Intel(R) Core(TM) i7-10700K",
        "cores": 8,
        "threads": 16
    }

    model = CPUConfig(**data)

    assert model.model == "Intel(R) Core(TM) i7-10700K"
    assert model.cores == 8
    assert model.threads == 16


def test_memory_config():
    """Test MemoryConfig model."""
    data = {
        "total": 34359738368,  # 32 GB
        "used": 17179869184,   # 16 GB
        "free": 17179869184    # 16 GB
    }

    model = MemoryConfig(**data)

    assert model.total == 34359738368
    assert model.used == 17179869184
    assert model.free == 17179869184


def test_display_config():
    """Test DisplayConfig model."""
    data = {
        "branding": "Unraid",
        "theme": "black",
        "language": "en_US"
    }

    model = DisplayConfig(**data)

    assert model.branding == "Unraid"
    assert model.theme == "black"
    assert model.language == "en_US"


def test_email_config():
    """Test EmailConfig model."""
    data = {
        "enabled": True,
        "to": "user@example.com",
        "from": "unraid@example.com",
        "server": "smtp.example.com",
        "port": 587,
        "secure": True,
        "authType": "plain",
        "username": "unraid"
    }

    model = EmailConfig(**data)

    assert model.enabled is True
    assert model.to == "user@example.com"
    assert model.from_field == "unraid@example.com"
    assert model.server == "smtp.example.com"
    assert model.port == 587
    assert model.secure is True
    assert model.authType == "plain"
    assert model.username == "unraid"


def test_email_config_minimal():
    """Test EmailConfig model with minimal data."""
    data = {
        "enabled": False,
        "secure": False
    }

    model = EmailConfig(**data)

    assert model.enabled is False
    assert model.to is None
    assert model.from_field is None
    assert model.server is None
    assert model.port is None
    assert model.secure is False
    assert model.authType is None
    assert model.username is None


def test_pushover_config():
    """Test PushoverConfig model."""
    data = {
        "enabled": True,
        "userKey": "user-key",
        "appKey": "app-key"
    }

    model = PushoverConfig(**data)

    assert model.enabled is True
    assert model.userKey == "user-key"
    assert model.appKey == "app-key"


def test_pushover_config_minimal():
    """Test PushoverConfig model with minimal data."""
    data = {
        "enabled": False
    }

    model = PushoverConfig(**data)

    assert model.enabled is False
    assert model.userKey is None
    assert model.appKey is None


def test_notification_agents():
    """Test NotificationAgents model."""
    data = {
        "arrayStart": True,
        "arrayStop": True,
        "diskWarning": True,
        "cpuWarning": False,
        "memoryWarning": False,
        "updateAvailable": True
    }

    model = NotificationAgents(**data)

    assert model.arrayStart is True
    assert model.arrayStop is True
    assert model.diskWarning is True
    assert model.cpuWarning is False
    assert model.memoryWarning is False
    assert model.updateAvailable is True


def test_notifications_config():
    """Test NotificationsConfig model."""
    data = {
        "email": {
            "enabled": True,
            "secure": True
        },
        "pushover": {
            "enabled": False
        },
        "agents": {
            "arrayStart": True,
            "arrayStop": True,
            "diskWarning": True,
            "cpuWarning": False,
            "memoryWarning": False,
            "updateAvailable": True
        }
    }

    model = NotificationsConfig(**data)

    assert model.email.enabled is True
    assert model.email.secure is True
    assert model.pushover.enabled is False
    assert model.agents.arrayStart is True
    assert model.agents.arrayStop is True
    assert model.agents.diskWarning is True
    assert model.agents.cpuWarning is False
    assert model.agents.memoryWarning is False
    assert model.agents.updateAvailable is True


def test_vm_config():
    """Test VMConfig model."""
    data = {
        "enabled": True,
        "isolatedCpuPinning": True,
        "pciPassthrough": True
    }

    model = VMConfig(**data)

    assert model.enabled is True
    assert model.isolatedCpuPinning is True
    assert model.pciPassthrough is True


def test_docker_config():
    """Test DockerConfig model."""
    data = {
        "enabled": True,
        "auto": True,
        "image": "ubuntu:latest",
        "privileged": False
    }

    model = DockerConfig(**data)

    assert model.enabled is True
    assert model.auto is True
    assert model.image == "ubuntu:latest"
    assert model.privileged is False


def test_docker_config_minimal():
    """Test DockerConfig model with minimal data."""
    data = {
        "enabled": False,
        "auto": False,
        "privileged": False
    }

    model = DockerConfig(**data)

    assert model.enabled is False
    assert model.auto is False
    assert model.image is None
    assert model.privileged is False


def test_shares_config():
    """Test SharesConfig model."""
    data = {
        "enableNetbios": True,
        "enableWsd": False,
        "enableAvahi": True,
        "localMaster": True,
        "security": "public"
    }

    model = SharesConfig(**data)

    assert model.enableNetbios is True
    assert model.enableWsd is False
    assert model.enableAvahi is True
    assert model.localMaster is True
    assert model.security == "public"


def test_ftp_config():
    """Test FTPConfig model."""
    data = {
        "enabled": True,
        "port": 21,
        "allowReset": False,
        "publicAccess": False
    }

    model = FTPConfig(**data)

    assert model.enabled is True
    assert model.port == 21
    assert model.allowReset is False
    assert model.publicAccess is False


def test_dynamic_dns_config():
    """Test DynamicDNSConfig model."""
    data = {
        "enabled": True,
        "service": "duckdns",
        "domain": "example.duckdns.org",
        "username": "user"
    }

    model = DynamicDNSConfig(**data)

    assert model.enabled is True
    assert model.service == "duckdns"
    assert model.domain == "example.duckdns.org"
    assert model.username == "user"


def test_dynamic_dns_config_minimal():
    """Test DynamicDNSConfig model with minimal data."""
    data = {
        "enabled": False
    }

    model = DynamicDNSConfig(**data)

    assert model.enabled is False
    assert model.service is None
    assert model.domain is None
    assert model.username is None


def test_tunable_config():
    """Test TunableConfig model."""
    data = {
        "cacheDirectoryMethod": "most-free",
        "cacheNoCache": True,
        "sharesMissingEnable": True,
        "shareNfsEnable": True,
        "shareNfsGuest": False,
        "shareNfsSecure": True,
        "shareAftpEnable": False,
        "shareAftpPublicEnable": False,
        "shareAftpSecure": True
    }

    model = TunableConfig(**data)

    assert model.cacheDirectoryMethod == "most-free"
    assert model.cacheNoCache is True
    assert model.sharesMissingEnable is True
    assert model.shareNfsEnable is True
    assert model.shareNfsGuest is False
    assert model.shareNfsSecure is True
    assert model.shareAftpEnable is False
    assert model.shareAftpPublicEnable is False
    assert model.shareAftpSecure is True


def test_tunable_config_minimal():
    """Test TunableConfig model with minimal data."""
    data = {
        "sharesMissingEnable": False,
        "shareNfsEnable": False,
        "shareNfsGuest": False,
        "shareNfsSecure": False,
        "shareAftpEnable": False,
        "shareAftpPublicEnable": False,
        "shareAftpSecure": False
    }

    model = TunableConfig(**data)

    assert model.cacheDirectoryMethod is None
    assert model.cacheNoCache is None
    assert model.sharesMissingEnable is False
    assert model.shareNfsEnable is False
    assert model.shareNfsGuest is False
    assert model.shareNfsSecure is False
    assert model.shareAftpEnable is False
    assert model.shareAftpPublicEnable is False
    assert model.shareAftpSecure is False


def test_updates_config():
    """Test UpdatesConfig model."""
    data = {
        "auto": True,
        "autoNerdpack": True,
        "autoDocker": True,
        "autoPlugins": False,
        "autoCommunityApplications": True
    }

    model = UpdatesConfig(**data)

    assert model.auto is True
    assert model.autoNerdpack is True
    assert model.autoDocker is True
    assert model.autoPlugins is False
    assert model.autoCommunityApplications is True


def test_system_config():
    """Test SystemConfig model."""
    data = {
        "hostname": "unraid-server",
        "description": "My Unraid Server",
        "model": "Custom Build",
        "version": "6.12.0",
        "motherboard": "ASUS ROG STRIX Z590-E GAMING",
        "cpu": {
            "model": "Intel(R) Core(TM) i7-10700K",
            "cores": 8,
            "threads": 16
        },
        "memory": {
            "total": 34359738368,
            "used": 17179869184,
            "free": 17179869184
        },
        "network": {
            "interfaces": [
                {
                    "name": "eth0",
                    "mac": "00:11:22:33:44:55",
                    "up": True
                }
            ],
            "dnsServers": ["8.8.8.8", "8.8.4.4"],
            "hostname": "unraid-server"
        },
        "display": {
            "branding": "Unraid",
            "theme": "black",
            "language": "en_US"
        },
        "timezone": "UTC",
        "notifications": {
            "email": {
                "enabled": True,
                "secure": True
            },
            "pushover": {
                "enabled": False
            },
            "agents": {
                "arrayStart": True,
                "arrayStop": True,
                "diskWarning": True,
                "cpuWarning": False,
                "memoryWarning": False,
                "updateAvailable": True
            }
        },
        "vm": {
            "enabled": True,
            "isolatedCpuPinning": True,
            "pciPassthrough": True
        },
        "docker": {
            "enabled": True,
            "auto": True,
            "privileged": False
        },
        "shares": {
            "enableNetbios": True,
            "enableWsd": False,
            "enableAvahi": True,
            "localMaster": True,
            "security": "public"
        },
        "ftp": {
            "enabled": True,
            "port": 21,
            "allowReset": False,
            "publicAccess": False
        },
        "dynamicDns": {
            "enabled": False
        },
        "tunable": {
            "sharesMissingEnable": False,
            "shareNfsEnable": False,
            "shareNfsGuest": False,
            "shareNfsSecure": False,
            "shareAftpEnable": False,
            "shareAftpPublicEnable": False,
            "shareAftpSecure": False
        },
        "updates": {
            "auto": True,
            "autoNerdpack": True,
            "autoDocker": True,
            "autoPlugins": False,
            "autoCommunityApplications": True
        }
    }

    model = SystemConfig(**data)

    assert model.hostname == "unraid-server"
    assert model.description == "My Unraid Server"
    assert model.model == "Custom Build"
    assert model.version == "6.12.0"
    assert model.motherboard == "ASUS ROG STRIX Z590-E GAMING"
    assert model.cpu.model == "Intel(R) Core(TM) i7-10700K"
    assert model.cpu.cores == 8
    assert model.cpu.threads == 16
    assert model.memory.total == 34359738368
    assert model.memory.used == 17179869184
    assert model.memory.free == 17179869184
    assert len(model.network.interfaces) == 1
    assert model.network.interfaces[0].name == "eth0"
    assert model.network.interfaces[0].mac == "00:11:22:33:44:55"
    assert model.network.interfaces[0].up is True
    assert model.network.dnsServers == ["8.8.8.8", "8.8.4.4"]
    assert model.network.hostname == "unraid-server"
    assert model.display.branding == "Unraid"
    assert model.display.theme == "black"
    assert model.display.language == "en_US"
    assert model.timezone == "UTC"
    assert model.notifications.email.enabled is True
    assert model.notifications.email.secure is True
    assert model.notifications.pushover.enabled is False
    assert model.notifications.agents.arrayStart is True
    assert model.notifications.agents.arrayStop is True
    assert model.notifications.agents.diskWarning is True
    assert model.notifications.agents.cpuWarning is False
    assert model.notifications.agents.memoryWarning is False
    assert model.notifications.agents.updateAvailable is True
    assert model.vm.enabled is True
    assert model.vm.isolatedCpuPinning is True
    assert model.vm.pciPassthrough is True
    assert model.docker.enabled is True
    assert model.docker.auto is True
    assert model.docker.privileged is False
    assert model.shares.enableNetbios is True
    assert model.shares.enableWsd is False
    assert model.shares.enableAvahi is True
    assert model.shares.localMaster is True
    assert model.shares.security == "public"
    assert model.ftp.enabled is True
    assert model.ftp.port == 21
    assert model.ftp.allowReset is False
    assert model.ftp.publicAccess is False
    assert model.dynamicDns.enabled is False
    assert model.tunable.sharesMissingEnable is False
    assert model.tunable.shareNfsEnable is False
    assert model.tunable.shareNfsGuest is False
    assert model.tunable.shareNfsSecure is False
    assert model.tunable.shareAftpEnable is False
    assert model.tunable.shareAftpPublicEnable is False
    assert model.tunable.shareAftpSecure is False
    assert model.updates.auto is True
    assert model.updates.autoNerdpack is True
    assert model.updates.autoDocker is True
    assert model.updates.autoPlugins is False
    assert model.updates.autoCommunityApplications is True


def test_share_config():
    """Test ShareConfig model."""
    data = {
        "name": "media",
        "comment": "Media files",
        "allocator": "highwater",
        "fsType": "xfs",
        "include": "*.mp4,*.mkv",
        "exclude": "*.tmp",
        "useCache": "yes",
        "exportEnabled": True,
        "security": "public",
        "accessMode": "read-write",
        "ownership": "user",
        "diskIds": ["disk1", "disk2"]
    }

    model = ShareConfig(**data)

    assert model.name == "media"
    assert model.comment == "Media files"
    assert model.allocator == "highwater"
    assert model.fsType == "xfs"
    assert model.include == "*.mp4,*.mkv"
    assert model.exclude == "*.tmp"
    assert model.useCache == "yes"
    assert model.exportEnabled is True
    assert model.security == "public"
    assert model.accessMode == "read-write"
    assert model.ownership == "user"
    assert model.diskIds == ["disk1", "disk2"]


def test_share_config_minimal():
    """Test ShareConfig model with minimal data."""
    data = {
        "name": "media",
        "allocator": "highwater",
        "fsType": "xfs",
        "exportEnabled": True,
        "security": "public",
        "accessMode": "read-write",
        "ownership": "user"
    }

    model = ShareConfig(**data)

    assert model.name == "media"
    assert model.comment is None
    assert model.allocator == "highwater"
    assert model.fsType == "xfs"
    assert model.include is None
    assert model.exclude is None
    assert model.useCache is None
    assert model.exportEnabled is True
    assert model.security == "public"
    assert model.accessMode == "read-write"
    assert model.ownership == "user"
    assert model.diskIds == []


def test_plugin_config():
    """Test PluginConfig model."""
    data = {
        "name": "dynamix",
        "version": "1.0.0",
        "author": "Lime Technology, Inc.",
        "description": "Dynamix webGUI",
        "support": "https://lime-technology.com",
        "icon": "dynamix.png",
        "settings": {
            "theme": "black",
            "language": "en_US"
        }
    }

    model = PluginConfig(**data)

    assert model.name == "dynamix"
    assert model.version == "1.0.0"
    assert model.author == "Lime Technology, Inc."
    assert model.description == "Dynamix webGUI"
    assert model.support == "https://lime-technology.com"
    assert model.icon == "dynamix.png"
    assert model.settings == {"theme": "black", "language": "en_US"}


def test_plugin_config_minimal():
    """Test PluginConfig model with minimal data."""
    data = {
        "name": "dynamix",
        "version": "1.0.0",
        "author": "Lime Technology, Inc."
    }

    model = PluginConfig(**data)

    assert model.name == "dynamix"
    assert model.version == "1.0.0"
    assert model.author == "Lime Technology, Inc."
    assert model.description is None
    assert model.support is None
    assert model.icon is None
    assert model.settings == {}


def test_mutation_response():
    """Test MutationResponse model."""
    data = {
        "success": True,
        "message": "Operation completed successfully"
    }

    model = MutationResponse(**data)

    assert model.success is True
    assert model.message == "Operation completed successfully"


def test_mutation_response_minimal():
    """Test MutationResponse model with minimal data."""
    data = {
        "success": False
    }

    model = MutationResponse(**data)

    assert model.success is False
    assert model.message is None


def test_validation_error():
    """Test validation error."""
    with pytest.raises(ValidationError):
        # Missing required field 'up'
        NetworkInterface(name="eth0", mac="00:11:22:33:44:55")
