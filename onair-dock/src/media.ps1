# Prints one JSON line every 2 seconds describing what Windows is playing
# (Spotify, browsers, Apple Music, etc.) using the Windows media session API.
# Reads commands from stdin: "toggle", "next", "prev".
$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
  $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
  $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
})[0]

function Await($op, [Type]$type) {
  $task = $asTaskGeneric.MakeGenericMethod($type).Invoke($null, @($op))
  $null = $task.Wait(5000)
  return $task.Result
}

$null = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager, Windows.Media.Control, ContentType = WindowsRuntime]
$mgrType = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]
$propsType = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties]
$mgr = Await ($mgrType::RequestAsync()) $mgrType

if (-not $mgr) {
  Write-Output '{"error":"unavailable"}'
  exit 1
}

# A StreamReader over the raw stdin stream gives a truly async ReadLineAsync
# ([Console]::In would block the loop).
$stdin = New-Object System.IO.StreamReader([Console]::OpenStandardInput())
$pending = $stdin.ReadLineAsync()

while ($true) {
  if ($pending.IsCompleted) {
    $cmd = $pending.Result
    if ($null -eq $cmd) { exit 0 }  # parent closed stdin
    $session = $mgr.GetCurrentSession()
    if ($session) {
      switch ($cmd.Trim()) {
        'toggle' { $null = $session.TryTogglePlayPauseAsync() }
        'next'   { $null = $session.TrySkipNextAsync() }
        'prev'   { $null = $session.TrySkipPreviousAsync() }
      }
    }
    $pending = $stdin.ReadLineAsync()
    Start-Sleep -Milliseconds 300
  }

  $session = $mgr.GetCurrentSession()
  if ($session) {
    $props = Await ($session.TryGetMediaPropertiesAsync()) $propsType
    $status = $session.GetPlaybackInfo().PlaybackStatus.ToString()
    $obj = [ordered]@{
      title  = [string]$props.Title
      artist = [string]$props.Artist
      status = $status
      app    = [string]$session.SourceAppUserModelId
    }
    Write-Output ($obj | ConvertTo-Json -Compress)
  } else {
    Write-Output '{}'
  }
  Start-Sleep -Milliseconds 1700
}
