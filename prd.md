# Product Requirement Document (PRD)

## Product Name

Opportunity OS

## Objective

Build a system that identifies, ranks, and delivers relevant opportunities (jobs, schemes, training) to users using AI and backend intelligence, without requiring active search or high digital literacy.

## Problem Statement

* Users are unaware of opportunities they are eligible for
* Information is fragmented and complex
* Low digital literacy limits access
* No personalization in existing systems

## Target Users

* Rural / semi-urban individuals
* e-Sevai operators / NGOs
* Low to medium digital literacy users

## Core Features

### 1. Opportunity Ingestion

* Add schemes, jobs, training programs
* Manual input (admin)

### 2. AI Processing

* Classify opportunity type
* Extract eligibility criteria
* Simplify content

### 3. User Profiles

* Phone number (OTP simulated)
* Age, occupation, pincode

### 4. Matching Engine

* Match users with opportunities
* Based on eligibility + location

### 5. Ranking System

* Score opportunities using:

  * relevance
  * urgency
  * location

### 6. Delivery System

* Receipt-style output (UI simulation)
* Voice output (audio playback)
* Operator dashboard

## Non-Goals

* No real Aadhaar integration
* No real government DB access
* No full WhatsApp/IVR integration (simulate only)

## Success Metrics

* Accurate matching (relevance)
* Clear demo flow
* Multi-channel output working
* Minimal latency in processing

## Constraints

* Hackathon time limit
* Limited dataset (mock + few real samples)
* Must work offline-friendly (Ollama)
