```sh
# Windows Partition Manager

A powerful and user-friendly GUI application for managing disk partitions on Windows 10. Built with Python and modern Windows disk management tools.

## Features

- **Disk Management**
  - List all physical disks and their properties
  - Display detailed disk information
  - Convert between MBR and GPT disk types
  - Real-time disk status updates

- **Partition Operations**
  - Create new partitions
  - Delete existing partitions
  - Extend partitions with specific sizes
  - Shrink partitions
  - View partition details
  - Display partition file system and free space

- **Advanced Features**
  - Detailed disk and partition information
  - Support for both basic and dynamic disks
  - Error handling and data safety warnings
  - Administrator privilege management
  - Real-time operation feedback

## Requirements

- Windows 10 or later
- Administrator privileges
- At least 100MB free disk space
- 4GB RAM recommended

## Installation

1. Download the latest release (`Windows Partition Manager.exe`)
2. Right-click the executable and select "Run as administrator"
3. Allow the application when prompted for administrator privileges

## Usage

### Basic Operations

1. **View Disks**
   - Launch the application
   - All available disks will be displayed in the main window

2. **View Partitions**
   - Select a disk from the list
   - Partitions will be displayed with their properties

3. **Create Partition**
   - Select a disk
   - Click "Create Partition"
   - Enter the desired size in MB
   - Follow the prompts

4. **Extend Partition**
   - Select the partition to extend
   - Click "Extend Partition"
   - Enter the amount to extend in MB
   - Confirm the operation

### Advanced Operations

1. **Shrink Partition**
   - Select the partition
   - Click "Shrink Partition" in Advanced Options
   - Enter the amount to shrink in MB
   - Review warnings and confirm

2. **Convert Disk**
   - Select the disk
   - Click "Convert Disk" in Advanced Options
   - Choose between GPT and MBR
   - WARNING: This will erase all data on the disk

## Safety Precautions

- **ALWAYS BACKUP YOUR DATA** before performing any partition operations
- Verify selections carefully before confirming operations
- Do not interrupt operations while in progress
- Keep power supply stable during operations
- Read all warning messages carefully

## Troubleshooting

1. **Application won't start**
   - Verify you're running as administrator
   - Check Windows event logs for errors

2. **Operations fail**
   - Ensure disk is not in use
   - Check for sufficient free space
   - Verify disk is not locked by other applications

3. **Disk not showing**
   - Refresh disk list
   - Verify disk is properly connected
   - Check disk in Windows Disk Management

## Developer Information

- **Developer:** KAMRUL MOLLAH
- **Contact:** 01990646194
- **Website:** [kamrulmollah.com](https://kamrulmollah.com)

## Legal Notice

This software modifies disk partitions which can result in data loss if not used properly. The developer is not responsible for any data loss or system damage resulting from the use of this software.

## Version History

- v1.0.0 (2024)
  - Initial release
  - Basic partition management
  - Advanced disk operations
  - GUI interface

## Support

For support, bug reports, or feature requests:
- Visit: [kamrulmollah.com](https://kamrulmollah.com)
- Contact the developer directly

---

© 2024 KAMRUL MOLLAH. All rights reserved.
```