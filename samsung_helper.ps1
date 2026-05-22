# Script PowerShell para gerenciar dispositivos Samsung
# Detecta porta COM e reseta drivers USB

function Get-SamsungModemPort {
    try {
        $devices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object { 
            $_.InstanceId -like "*USB\VID_04E8*" -and $_.Class -eq "Modem" 
        }
        if ($devices) {
            foreach ($dev in $devices) {
                $name = $dev.FriendlyName
                if ($name -match "COM(\d+)") {
                    return $matches[0]
                }
            }
        }
    } catch {
        Write-Output "Erro ao detectar porta: $_"
    }
    return $null
}

function Reset-SamsungUSBDrivers {
    try {
        $devices = Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like "*VID_04E8*" }
        if ($devices) {
            foreach ($dev in $devices) {
                Write-Output "Resetando driver: $($dev.FriendlyName)"
                Disable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1
                Enable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1
            }
            Write-Output "Drivers resetados com sucesso!"
        } else {
            Write-Output "Nenhum dispositivo Samsung encontrado"
        }
    } catch {
        Write-Output "Erro ao resetar drivers: $_"
    }
}

# Executa conforme argumentos
if ($args.Count -gt 0) {
    switch ($args[0]) {
        "detect" {
            $port = Get-SamsungModemPort
            if ($port) { Write-Output $port } else { Write-Output "NOT_FOUND" }
        }
        "reset" {
            Reset-SamsungUSBDrivers
        }
        default {
            Write-Output "Uso: .\\samsung_helper.ps1 [detect|reset]"
        }
    }
}
