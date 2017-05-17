;; global settings
(setq
 inhibit-startup-screen t
 create-lockfiles nil
 column-number-mode t
 scroll-error-top-bottom t
 show-paren-delay 0.2
 use-package-always-ensure t
 icomplete-mode t
 )

;; global default settings
(setq-default
 indent-tabs-mode t
 tab-width 2
 c-basic-offset 2
 )

;; global modes
(electric-indent-mode t)
(global-linum-mode t)

;; load and setup package macro
(require 'package)
(setq
 package-archives '(("gnu" . "https://elpa.gnu.org/packages/")
;                    ("marmalade" . "https://marmalade-repo.org/packages/")
                    ("melpa-stable" . "https://stable.melpa.org/packages/")
                    ("melpa" . "https://melpa.org/packages/")))
(package-initialize)

;; load use-package macro
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))
(when (not package-archive-contents)
  (package-refresh-contents)
  (package-install 'use-package))
(eval-when-compile
	(require 'use-package))

;; load other packages
(use-package ensime
  :pin melpa-stable)

(use-package projectile
  :demand
  :init   (setq projectile-use-git-grep t)
  :config (projectile-global-mode t)
  :bind   (("s-f" . projectile-find-file)
           ("s-F" . projectile-grep)))

(use-package dtrt-indent)

(use-package undo-tree
  :diminish undo-tree-mode
  :config (global-undo-tree-mode)
  :bind ("s-/" . undo-tree-visualize))

(use-package highlight-symbol
  :diminish highlight-symbol-mode
  :commands highlight-symbol
  :bind ("s-h" . highlight-symbol))

(use-package popup-imenu
  :commands popup-imenu
  :bind ("M-i" . popup-imenu))

(use-package magit
  :commands magit-status magit-blame
  :init (setq
         magit-revert-buffers nil)
  :bind (("s-g" . magit-status)
         ("s-b" . magit-blame)))

(use-package company
  :diminish company-mode
  :commands company-mode
  :init
  (setq
   company-dabbrev-ignore-case nil
   company-dabbrev-code-ignore-case nil
   company-dabbrev-downcase nil
   company-idle-delay 0
   company-minimum-prefix-length 4))
;;  :config
;;  ;; disables TAB in company-mode, freeing it for yasnippet
;;  (define-key company-active-map [tab] nil)
;;  (define-key company-active-map (kbd "TAB") nil))

(use-package smex
	:bind ("M-x" . smex))

(use-package drag-stuff
	:init (drag-stuff-global-mode 1)
	:bind (("M-N" . drag-stuff-down)
				 ("M-P" . drag-stuff-up)))

;; (use-package saveplace
;; 	:config (setq-default save-place t))

(use-package smartparens
	:init (progn
					(show-smartparens-global-mode t)
					(smartparens-global-mode t)))

(use-package yaml-mode
	:mode ("\\.yml$" . yaml-mode))


(use-package ibuffer
	:config (setq ibuffer-expert t)
	  :bind ("C-x C-b" . ibuffer))

(use-package helm)

(use-package clojure-mode)

(use-package chef-mode)

(use-package apache-mode)

(use-package nginx-mode)

(use-package git-commit)

(use-package gitconfig-mode)

(use-package gitignore-mode)

(use-package pandoc)

(use-package pandoc-mode)

(use-package rust-mode)

(use-package scala-mode2)

(use-package systemd)

(use-package thrift)

(use-package undo-tree)

(use-package protobuf-mode)

(use-package groovy-mode)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
	 (quote
		(protobuf-mode groovy-mode yaml-mode use-package undo-tree typescript-mode top-mode thrift systemd syslog-mode ssh-config-mode sqlup-mode shm scss-mode scala-mode2 rust-mode rainbow-mode qsimpleq-theme python-mode projectile popup-imenu pig-mode pandoc-mode pandoc nginx-mode moe-theme material-theme markdown-mode magit lua-mode log4j-mode jvm-mode json-mode jira jar-manifest-mode impatient-mode idris-mode hindent highlight-symbol helm graphene go-mode gitignore-mode gitconfig-mode git-blame fsharp-mode feature-mode espresso-theme ensime elm-mode elixir-mode dtrt-indent drag-stuff dockerfile-mode diff-hl cyberpunk-theme csv-mode csharp-mode crontab-mode company-ghc coffee-mode closure-lint-mode clojurescript-mode clojure-mode-extra-font-locking chef-mode butler basic-theme autopair auto-save-buffers-enhanced auto-indent-mode auto-complete apache-mode angular-mode ample-zen-theme ample-theme))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
