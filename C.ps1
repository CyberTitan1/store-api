Add-Type -AssemblyName System.Windows.Forms

# Get screen dimensions
$screenWidth  = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$screenHeight = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height

# Random scary phrases with Unicode escapes
$messages = @(
    "You have been hacked!",
    "System compromised `u{1F480}",   # 💀
    "Your files are mine `u{1F631}",  # 😱
    "Unauthorized access detected `u{26A0}", # ⚠️
    "Security breach `u{1F525}",      # 🔥
    "Malware unleashed `u{1F47E}"     # 👾
)

while ($true) {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Alert"

    # Random size
    $form.Width  = Get-Random -Minimum 150 -Maximum 250
    $form.Height = Get-Random -Minimum 80 -Maximum 150

    # Random position
    $form.StartPosition = "Manual"
    $form.Left = Get-Random -Minimum 0 -Maximum ($screenWidth - $form.Width)
    $form.Top  = Get-Random -Minimum 0 -Maximum ($screenHeight - $form.Height)

    # Random scary text
    $label = New-Object System.Windows.Forms.Label
    $label.Text = $messages[(Get-Random -Minimum 0 -Maximum $messages.Count)]
    $label.AutoSize = $true
    $label.Left = 10
    $label.Top  = 10
    $form.Controls.Add($label)

    # Show and force redraw so text appears immediately
    $form.Show()
    $form.Refresh()
}
