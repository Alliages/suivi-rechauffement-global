<#
.SYNOPSIS
    Exporte les images et/ou les GIF animés du suivi du réchauffement mondial.

.DESCRIPTION
    Deux façons de fonctionner :
      - par défaut : télécharge les fichiers précalculés chaque mois sur le site
        (aucune installation nécessaire, réglages fixes) ;
      - avec -Local : génère les images sur ce poste avec Python, avec tous les
        réglages (période, pas, format, taille, langue, vitesse du GIF).
        Python 3.10+ est requis ; les paquets sont installés automatiquement dans
        un environnement virtuel (.venv) à côté du script.

.EXAMPLE
    .\export.ps1
    # GIF + images des deux animations, versions précalculées, dans .\exports

.EXAMPLE
    .\export.ps1 -Mode gif -Animation extrapolation
    # seulement le GIF de l'extrapolation (précalculé)

.EXAMPLE
    .\export.ps1 -Local -Mode frames -Animation courbe -Debut 2000-01 -Pas 1 -Format svg -Dossier .\images
    # toutes les images de la courbe depuis 2000, en SVG, dans .\images

.EXAMPLE
    .\export.ps1 -Local -Mode gif -Animation both -Debut 2010-01 -Pas 2 -Fps 6 -Largeur 1920 -Hauteur 1080 -Langue en
#>
[CmdletBinding()]
param(
    # ---- Que produire -----------------------------------------------------
    [ValidateSet('frames', 'gif', 'both')]
    [string]$Mode = 'both',                     # images, GIF ou les deux
    [ValidateSet('courbe', 'extrapolation', 'both')]
    [string]$Animation = 'both',                # quelle(s) animation(s)

    # ---- Génération locale (ignorés sans -Local) --------------------------
    [switch]$Local,                             # générer sur ce poste avec Python
    [string]$Debut,                             # premier mois AAAA-MM (vide = défaut)
    [string]$Fin,                               # dernier mois AAAA-MM (vide = dernier dispo)
    [ValidateRange(1, 120)]
    [int]$Pas = 1,                              # un mois sur N
    [ValidateRange(0.5, 50)]
    [double]$Fps = 8,                           # images par seconde du GIF
    [ValidateSet('png', 'svg', 'jpg', 'pdf')]
    [string]$Format = 'png',                    # format des images
    [int]$Largeur = 1280,                       # pixels
    [int]$Hauteur = 720,                        # pixels
    [ValidateSet('fr', 'en')]
    [string]$Langue = 'fr',

    # ---- Emplacements -----------------------------------------------------
    [string]$Dossier = '.\exports',             # dossier de sortie
    [string]$SiteUrl = 'https://alliages.github.io/suivi-rechauffement-global',
    [string]$RawUrl = 'https://raw.githubusercontent.com/Alliages/suivi-rechauffement-global/main'
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'        # Invoke-WebRequest beaucoup plus rapide
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'

$Animations = if ($Animation -eq 'both') { @('courbe', 'extrapolation') } else { @($Animation) }
New-Item -ItemType Directory -Force -Path $Dossier | Out-Null
$Dossier = (Resolve-Path $Dossier).Path

# ==========================================================================
# Mode 1 : téléchargement des fichiers précalculés
# ==========================================================================
# Réglages passés explicitement (pour prévenir s'ils sont ignorés sans -Local)
$Custom = @('Debut', 'Fin', 'Pas', 'Fps', 'Format', 'Largeur', 'Hauteur', 'Langue') |
    Where-Object { $PSBoundParameters.ContainsKey($_) }

function Get-Precalcule {
    $custom = $script:Custom
    if ($custom) {
        Write-Warning ("Réglages ignorés sans -Local : " + ($custom -join ', ') +
                       ". Ajoute -Local pour les appliquer.")
    }
    $manifest = Invoke-RestMethod "$SiteUrl/exports/manifest.json"
    foreach ($anim in $Animations) {
        if ($Mode -in 'gif', 'both') {
            $name = $manifest."$($anim)_gif"
            Write-Host "Téléchargement de $name..."
            Invoke-WebRequest "$SiteUrl/exports/$name" -OutFile (Join-Path $Dossier $name)
        }
        if ($Mode -in 'frames', 'both') {
            $zip = $manifest."$($anim)_zip"
            $tmp = Join-Path $env:TEMP $zip
            Write-Host "Téléchargement de $zip..."
            Invoke-WebRequest "$SiteUrl/exports/$zip" -OutFile $tmp
            $dest = Join-Path $Dossier "images_$anim"
            if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
            Expand-Archive $tmp -DestinationPath $dest
            Remove-Item $tmp
        }
    }
}

# ==========================================================================
# Mode 2 : génération locale avec Python
# ==========================================================================
function Find-Python {
    foreach ($cmd in @(@('py', '-3'), @('python'), @('python3'))) {
        $exe = Get-Command $cmd[0] -ErrorAction SilentlyContinue
        if ($exe) {
            $pyArgs = @($cmd | Select-Object -Skip 1)
            $ver = & $exe.Source @pyArgs -c "import sys; print(sys.version_info >= (3, 10))" 2>$null
            if ($ver -eq 'True') { return @{ Exe = $exe.Source; Args = $pyArgs } }
        }
    }
    throw "Python 3.10 ou plus récent est introuvable. Installe-le depuis https://www.python.org/ ou utilise le mode sans -Local."
}

function Get-Pipeline {
    # Script lancé depuis le dépôt cloné : on utilise ..\pipeline
    $repoPipeline = Join-Path $PSScriptRoot '..\pipeline'
    if (Test-Path (Join-Path $repoPipeline 'render.py')) { return (Resolve-Path $repoPipeline).Path }
    # Sinon : on télécharge render.py et config.py dans un dossier à côté du script
    $dir = Join-Path $PSScriptRoot 'pipeline'
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    foreach ($f in 'render.py', 'config.py') {
        Invoke-WebRequest "$RawUrl/pipeline/$f" -OutFile (Join-Path $dir $f)
    }
    return $dir
}

function Invoke-Local {
    $py = Find-Python
    $venv = Join-Path $PSScriptRoot '.venv'
    $venvPy = Join-Path $venv 'Scripts\python.exe'
    if (-not (Test-Path $venvPy)) { $venvPy = Join-Path $venv 'bin/python' }   # macOS / Linux
    if (-not (Test-Path $venvPy)) {
        Write-Host "Création de l'environnement Python (une seule fois)..."
        $pyArgs = $py.Args
        & $py.Exe @pyArgs -m venv $venv
        $venvPy = if (Test-Path (Join-Path $venv 'Scripts\python.exe')) { Join-Path $venv 'Scripts\python.exe' } else { Join-Path $venv 'bin/python' }
        & $venvPy -m pip install --quiet --upgrade pip
        & $venvPy -m pip install --quiet matplotlib pillow
    }
    $pipeline = Get-Pipeline

    $common = @(
        (Join-Path $pipeline 'render.py'),
        '--donnees', "$SiteUrl/data/series.json",       # toujours les données les plus récentes
        '--pas', $Pas, '--fps', $Fps.ToString([Globalization.CultureInfo]::InvariantCulture),
        '--format', $Format, '--largeur', $Largeur, '--hauteur', $Hauteur,
        '--langue', $Langue, '--sortie', $Dossier
    )
    if ($Debut) { $common += @('--debut', $Debut) }
    if ($Fin) { $common += @('--fin', $Fin) }
    if ($Mode -eq 'frames') { $common += '--pas-de-gif' }
    if ($Mode -eq 'gif') { $common += '--pas-d-images' }

    foreach ($anim in $Animations) {
        & $venvPy @common --animation $anim
        if ($LASTEXITCODE -ne 0) { throw "Échec du rendu ($anim)." }
    }
}

# ==========================================================================
if ($Local) { Invoke-Local } else { Get-Precalcule }
Write-Host "Terminé : $Dossier" -ForegroundColor Green
Get-ChildItem $Dossier | Format-Table Name, Length, LastWriteTime -AutoSize
