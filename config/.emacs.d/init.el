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
 c-basic-offset 1
 )

;; global modes
(electric-indent-mode t)
(global-linum-mode t)

;; load and setup package macro
(require 'package)
(setq
 package-archives '(("gnu" . "https://elpa.gnu.org/packages/")
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
  :pin melpa-stable
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
  :pin melpa-stable
  :diminish highlight-symbol-mode
  :commands highlight-symbol
  :bind ("s-h" . highlight-symbol))

(use-package popup-imenu
  :pin melpa-stable
  :commands popup-imenu
  :bind ("M-i" . popup-imenu))

(use-package magit
  :pin melpa-stable
  :commands magit-status magit-blame
  :init (setq
         magit-revert-buffers nil)
  :bind (("s-g" . magit-status)
         ("s-b" . magit-blame)))

(use-package company
  :pin melpa-stable
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
  :pin melpa-stable
	:bind ("M-x" . smex))

(use-package lua-mode)

(use-package drag-stuff
  :pin melpa-stable
	:init (drag-stuff-global-mode 1)
	:bind (("M-N" . drag-stuff-down)
				 ("M-P" . drag-stuff-up)))

;; (use-package saveplace
;; 	:config (setq-default save-place t))

(use-package smartparens
  :pin melpa-stable
	:init (progn
					(show-smartparens-global-mode t)
					(smartparens-global-mode t)))

(use-package yaml-mode
  :pin melpa-stable
	:mode ("\\.yml$" . yaml-mode))


(use-package ibuffer
  :pin melpa-stable
	:config (setq ibuffer-expert t)
	  :bind ("C-x C-b" . ibuffer))

(use-package helm
  :pin melpa-stable)

(use-package clojure-mode
  :pin melpa-stable)

(use-package chef-mode)

(use-package apache-mode)

(use-package nginx-mode)

(use-package git-commit
  :pin melpa-stable)

(use-package gitconfig-mode)

(use-package gitignore-mode)

(use-package pandoc
  :pin melpa-stable)

(use-package pandoc-mode
  :pin melpa-stable)

(use-package rust-mode)

(use-package systemd
  :pin melpa-stable)

(use-package thrift
  :pin melpa-stable)

(use-package undo-tree
  :pin melpa-stable)

(use-package groovy-mode)

(use-package go-mode)

(use-package protobuf-mode)
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
	 (quote
		(elixir-mode erlang php-mode markdown-mode markdown-mode+ markdown-preview-mode dockerfile-mode docker go-mode elm-mode elm-yasnippets yaml-mode use-package undo-tree thrift systemd smex smartparens rust-mode protobuf-mode projectile popup-imenu pandoc-mode pandoc nginx-mode magit lua-mode highlight-symbol helm groovy-mode gitignore-mode gitconfig-mode ensime dtrt-indent drag-stuff clojure-mode chef-mode apache-mode)))
 '(safe-local-variable-values (quote ((chef-mode . t)))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
